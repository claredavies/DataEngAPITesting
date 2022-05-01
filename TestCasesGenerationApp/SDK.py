"""
Test cases generation SDK implemented.

This class allows the user to train GPT-2 model and then get new/novel test cases.
It accepts .csv files.

"""

import sys,os,json,shutil,re,urllib.request,time
from tensorflow.python.client import device_lib
from src.accumulate import AccumulatingOptimizer
from tqdm import tqdm
import numpy as np
from sys import exit
from tensorflow.core.protobuf import rewriter_config_pb2
from src import model, sample, encoder
import tensorflow as tf
from datetime import datetime
from src.load_dataset import load_dataset, Sampler

tf.compat.v1.disable_eager_execution()


class TestCasesGenerator:
    """
    The main class the contains the functions to check status.
    """
    done: bool

    def _init(self):
        """
        Wrapper function that is mainly called by initialize.
        Mainly used to reset/initialize values
        :return:
        """
        self.done = False
        self.training = None
        self.generating = ""
        self.duration = 100
        self.duration_unit = 0

    def __init__(self):
        """
        initializing values
        """
        self._init()

    # Feature selection
    # Restler output file may contain duplicate requests.
    # This method eliminates duplicate ones and also extract the desired features. We just need request_type , request_uri and request body
    def process_restler_output(self, restler_raw_file='test_cases_produced.csv',
                               restler_processed_file="RESTler_unique_output.txt"):
        import csv, itertools
        file = open(restler_raw_file)
        csvreader = csv.reader(file)
        header = next(csvreader)
        print(header)
        rows = []
        for row in csvreader:
            rows.append(row)
        file.close()

        for row in rows:
            del row[5]
            del row[4]
            del row[0]

        rows = [list(tupl) for tupl in {tuple(item) for item in rows}]
        textfile = open(restler_processed_file, "w")
        firstLine = True
        for row in rows:
            if row[2]:
                element = "HTTP " + row[0] + " " + row[1] + " " + row[2]
            else:
                element = "HTTP " + row[0] + " " + row[1]
            if (firstLine):
                textfile.write(element)
                firstLine = False
            else:
                textfile.write("\n" + element)
        textfile.close()
        return restler_processed_file

    # It is needed to download the GPT-2 pre-trained model. there are four types:
    # 1. 124M (default)   2. 355M   3. 774M   4. 1558M
    # The last two models are large and cannot finetuned in the google Colab
    def get_model(self, model_type='124M'):

        # create the directory if not exist
        path = os.path.join('models', model_type)
        if not os.path.exists(path):
            os.makedirs(path)
            url = "https://openaipublic.blob.core.windows.net/gpt-2/models/" + model_type + "/" + "checkpoint"
            urllib.request.urlretrieve(url, os.path.join(path, "checkpoint"))
            url = "https://openaipublic.blob.core.windows.net/gpt-2/models/" + model_type + "/" + "encoder.json"
            urllib.request.urlretrieve(url, os.path.join(path, "encoder.json"))
            url = "https://openaipublic.blob.core.windows.net/gpt-2/models/" + model_type + "/" + "hparams.json"
            urllib.request.urlretrieve(url, os.path.join(path, "hparams.json"))
            url = "https://openaipublic.blob.core.windows.net/gpt-2/models/" + model_type + "/" + "model.ckpt.data-00000-of-00001"
            urllib.request.urlretrieve(url, os.path.join(path, "model.ckpt.data-00000-of-00001"))
            url = "https://openaipublic.blob.core.windows.net/gpt-2/models/" + model_type + "/" + "model.ckpt.index"
            urllib.request.urlretrieve(url, os.path.join(path, "model.ckpt.index"))
            url = "https://openaipublic.blob.core.windows.net/gpt-2/models/" + model_type + "/" + "model.ckpt.meta"
            urllib.request.urlretrieve(url, os.path.join(path, "model.ckpt.meta"))
            url = "https://openaipublic.blob.core.windows.net/gpt-2/models/" + model_type + "/" + "vocab.bpe"
            urllib.request.urlretrieve(url, os.path.join(path, "vocab.bpe"))

    # return Tensorflow session. A Session places the graph ops onto Devices, such as CPUs or GPUs, and provides methods to execute them.
    def tensorflow_session(self):
        config = tf.compat.v1.ConfigProto()
        config.gpu_options.allow_growth = True
        config.graph_options.rewrite_options.layout_optimizer = rewriter_config_pb2.RewriterConfig.OFF
        return tf.compat.v1.Session(config=config)

    # with fine tuning we can train the model on our specific dataset
    def fine_tuning(self, session,
                    restler_raw_file='test_cases_produced-4.csv',
                    steps=-1,
                    model_type='124M',
                    batch_size=1,
                    learning_rate=0.0001,
                    accumulate_gradients=5,
                    run_name='run1',
                    sample_length=1023,
                    only_train_transformer_layers=False,
                    optimizer='adam'):

        dataset = self.process_restler_output(restler_raw_file)

        checkpoint_path = os.path.join('checkpoint', run_name)

        try:
            os.makedirs(checkpoint_path)
        except:
            pass
        files = [f for f in os.listdir(checkpoint_path)]
        for file in ['hparams.json', 'encoder.json', 'vocab.bpe']:
            try:
                shutil.copyfile(os.path.join('models', model_type, file),
                                os.path.join(checkpoint_path, file))
            except FileNotFoundError as fnf_error:
                print("You need to download the GPT-2 model first via get_model()")
                raise (fnf_error)

        enc = encoder.get_encoder(checkpoint_path)
        hparams = model.default_hparams()
        with open(os.path.join(checkpoint_path, 'hparams.json')) as f:
            hparams.override_from_dict(json.load(f))

        if sample_length > hparams.n_ctx:
            raise ValueError(
                "Can't get samples longer than window size: %s" % hparams.n_ctx)

        context = tf.compat.v1.placeholder(tf.int32, [batch_size, None])
        gpus = []

        output = model.model(hparams=hparams, X=context, gpus=gpus, reuse=False)
        loss = tf.reduce_mean(
            input_tensor=tf.nn.sparse_softmax_cross_entropy_with_logits(
                labels=context[:, 1:], logits=output['logits'][:, :-1]))

        all_vars = [v for v in tf.compat.v1.trainable_variables() if 'model' in v.name]
        # For models larger than 124M, it is better to set only_train_transformer_layers= true
        train_vars = [v for v in all_vars if '/h' in v.name] if only_train_transformer_layers else all_vars

        if optimizer == 'adam':
            opt = tf.compat.v1.train.AdamOptimizer(learning_rate=learning_rate)
        elif optimizer == 'sgd':
            opt = tf.compat.v1.train.GradientDescentOptimizer(learning_rate=learning_rate)

        # for models larger than 124M, it is better to set accumulate_gradients = 1
        # accumulate_gradients = 1 means no accumulated grads
        if accumulate_gradients > 1:

            # It calculates the loss and gradients after each mini-batch, but instead of updating the model parameters, it waits and accumulates the gradients over consecutive batches.
            opt = AccumulatingOptimizer(
                opt=opt,
                var_list=train_vars)
            opt_reset = opt.reset()
            opt_compute = opt.compute_gradients(loss)
            opt_apply = opt.apply_gradients()
            summary_loss = tf.compat.v1.summary.scalar('loss', opt_apply)
        else:
            opt_grads = tf.gradients(ys=loss, xs=train_vars)
            opt_grads = list(zip(opt_grads, train_vars))
            opt_apply = opt.apply_gradients(opt_grads)
            summary_loss = tf.compat.v1.summary.scalar('loss', loss)

        summary_log = tf.compat.v1.summary.FileWriter(checkpoint_path)

        saver = tf.compat.v1.train.Saver(
            var_list=all_vars,
            max_to_keep=1)
        # execute the operation in the tensors
        session.run(tf.compat.v1.global_variables_initializer())
        ckpt = tf.train.latest_checkpoint(os.path.join('models', model_type))

        # Loading checkpoint
        saver.restore(session, ckpt)

        print('Loading dataset...')
        chunks = load_dataset(enc, dataset, 50000)
        data_sampler = Sampler(chunks)
        print('dataset has', data_sampler.total_size, 'tokens')
        print('Training...')
        counter = 1
        counter_path = os.path.join(checkpoint_path, 'counter')
        counter_base = counter

        def sample_batch():
            return [data_sampler.sample(1024) for _ in range(batch_size)]

        avg_loss = (0.0, 0.0)
        start_time = time.time()

        if steps:
            steps = int(steps)

        # saving the trained model checkpoints
        def save():
            try:
                os.makedirs(checkpoint_path)
            except:
                pass
            print('Saving', os.path.join(checkpoint_path, 'model-{}').format(counter - 1))
            saver.save(
                session,
                os.path.join(checkpoint_path, 'model'),
                global_step=counter - 1)
            with open(counter_path, 'w') as fp:
                fp.write(str(counter - 1) + '\n')

        while True:
            if steps > 0 and counter == (counter_base + steps):
                save()
                return

            if accumulate_gradients > 1:
                # execute the operation in the tensors
                session.run(opt_reset)
                for _ in range(accumulate_gradients):
                    session.run(
                        opt_compute, feed_dict={context: sample_batch()})
                (v_loss, v_summary) = session.run((opt_apply, summary_loss))
            else:
                (_, v_loss, v_summary) = session.run(
                    (opt_apply, loss, summary_loss),
                    feed_dict={context: sample_batch()})

            summary_log.add_summary(v_summary, counter)

            if counter % 20 == 0:
                avg_loss = (avg_loss[0] * 0.99 + v_loss,
                            avg_loss[1] * 0.99 + 1.0)

                print(
                    '[{counter} | {time:2.2f}] loss={loss:2.2f} avg={avg:2.2f}'
                        .format(
                        counter=counter,
                        time=time.time() - start_time,
                        loss=v_loss,
                        avg=avg_loss[0] / avg_loss[1]))

            counter += 1

    def generate(self, session,
                 run_name='run1',
                 model_type=None,
                 model_novel_output_file='model_output_novel_t7_le5000.txt',
                 restler_processed_output_file='RESTler_unique_output.txt',
                 prefix=None,
                 seed=None,
                 nsamples=1,
                 batch_size=1,
                 length=1023,
                 temperature=0.7,
                 top_k=0,
                 top_p=0.0,
                 include_prefix=True,
                 overwrite=False):

        if batch_size is None:
            batch_size = 1
        assert nsamples % batch_size == 0

        if prefix == '':
            prefix = None

        if model_type:
            checkpoint_path = os.path.join('models', model_type)
        else:
            checkpoint_path = os.path.join('checkpoint', run_name)
        # We should convert words(tokens) to numbers as model cannot understand texts.
        # This vector of numbers capture some of meaning of word.
        enc = encoder.get_encoder(checkpoint_path)
        hparams = model.default_hparams()
        with open(os.path.join(checkpoint_path, 'hparams.json')) as f:
            hparams.override_from_dict(json.load(f))

        if prefix:
            context = tf.compat.v1.placeholder(tf.int32, [batch_size, None])
            context_tokens = enc.encode(prefix)

        np.random.seed(seed)
        tf.compat.v1.set_random_seed(seed)

        output = sample.sample_sequence(
            hparams=hparams,
            length=min(length, 1023 - (len(context_tokens) if prefix else 0)),
            start_token=enc.encoder['<|endoftext|>'] if not prefix else None,
            context=context if prefix else None,
            batch_size=batch_size,
            temperature=temperature, top_k=top_k, top_p=top_p
        )[:, 1:]
        # If overwite is true it appends to the previous content
        if overwrite:
            f = open("model_output_raw.txt", 'a')
        else:
            f = open("model_output_raw.txt", 'w')

        generated = 0
        while generated < nsamples:
            if not prefix:
                # execute the operation in the tensors
                out = session.run(output)
            else:
                out = session.run(output, feed_dict={
                    context: batch_size * [context_tokens]
                })
            for i in range(batch_size):
                generated += 1
                gen_text = enc.decode(out[i])
                if prefix:
                    gen_text = enc.decode(context_tokens[:1]) + gen_text

                gen_text = gen_text.lstrip('\n')
                # After each sample it adds END_OF_SAMPLE to the output file
                f.write("{}\n{}".format(gen_text, "END_OF_SAMPLE\n"))

        f.close()

        # This file (model_output_raw.txt) contains all the output that our model generated.
        # We should process the file and extract just the novel and uniques ones. (model_output_unique.txt)

        with open("model_output_raw.txt", 'r') as f:
            lines = f.readlines()

        count = 0;
        for line in lines:
            if "END_OF_SAMPLE" in line:
                lines[count] = ""
                lines[count - 1] = ""
            count = count + 1

        model_output_unique = sorted(set(lines), key=lines.index)

        if model_output_unique[-1][-1:] == "\n":
            model_output_unique[-1] = model_output_unique[-1][:-1]

        with open('model_output_unique.txt', 'w') as rmdup:
            rmdup.writelines(model_output_unique)

        with open('model_output_unique.txt', 'r') as rmdup:
            model_output_unique = rmdup.readlines()

        # It is needed to compare the unique output of Restler and the model.
        # We remove all the sapce from these files so that the space does not mislead us for the comparison process

        # remove spaces
        model_compressed_requests = [line.replace(' ', '') for line in model_output_unique]

        with open(restler_processed_output_file, 'r') as f:
            lines = f.readlines()
        # remove spaces
        dataset_requests = [line.replace(' ', '') for line in lines]

        count = 0
        new_request_lines = []
        for model_request in model_compressed_requests:
            duplicate = False
            for dataset_request in dataset_requests:
                if model_request == dataset_request:
                    duplicate = True
            if duplicate == False:
                new_request_lines.append(count)
            count = count + 1

        new_requests_file = open(model_novel_output_file, "w")
        for line in new_request_lines:
            new_requests_file.write(model_output_unique[line])

    def train_model(self):
        self.get_model(model_type="124M")

        self.session = self.tensorflow_session()
        # with fine tuning we can train the model on our specific dataset
        self.fine_tuning(self.session,
                    restler_raw_file='test_cases_produced.csv',
                    model_type='124M',
                    steps=100,
                    run_name='run')

    def generate_test_cases(self):
        # This will predict the next strings after the prefix
        # The lenght specify the size of each sample
        # Higher temperature results in more random completions. temperature=0 the model will become deterministic.
        # If overwrite is True, it concatenates the generated requests to the previous one.
        self.generate(self.session,
                 length=5000,
                 temperature=0.7,
                 prefix="HTTP GET",
                 nsamples=20,
                 batch_size=5,
                 overwrite=True
                 )

    def run_pipeline(self):
        self.train_model()
        self.generate_test_cases()

    def save_to_directory(self, directory_name):
        """
        Save the result to
        :return:
        """
        file1 = open(directory_name, "w")
        file1.write(self.result)
        self.result = ""
