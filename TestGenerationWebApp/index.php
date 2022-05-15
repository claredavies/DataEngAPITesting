 <?php
        if(isset($_POST['submit']))
        {
                ob_implicit_flush(true);
                ob_end_flush();

                $cmd = "bash /var/www/html/command.sh";

                $descriptorspec = array(
                0 => array("pipe", "r"),   // stdin is a pipe that the child will read from
                1 => array("pipe", "w"),   // stdout is a pipe that the child will write to
                2 => array("pipe", "w")    // stderr is a pipe that the child will write to
                );


                $process = proc_open($cmd, $descriptorspec, $pipes, realpath('./'), array());

        if (is_resource($process)) {

        while ($s = fgets($pipes[1])) {
                print $s;
   } }
}

?>
 
 <!DOCTYPE html>
 <html lang="en">
 <head>
  <meta charset="UTF-8">
  <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.5/css/bootstrap.min.css">
  <script src="https://ajax.googleapis.com/ajax/libs/jquery/2.1.3/jquery.min.js"></script>
  <script src="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.5/js/bootstrap.min.js"></script>
  <style type="text/css">
	#gpt2_form fieldset:not(:first-of-type) {
		display: none;
	}
  </style>
  <title>Testify Test Generator</title>
</head>
<body>
  <div class="container">
    <h1></h1>
	<div class="progress">
		<div class="progress-bar progress-bar-striped active" role="progressbar" aria-valuemin="0" aria-valuemax="100"></div>
	</div>
	
	<form id="gpt2_form" action=""  method="post">
	<fieldset>
		<h2>Step 1: Choose input file</h2>
		<div class="form-group">
		<input type="file" class="form-control-file" id="formControlInputFile">
	  </div>
		<input type="button" class="next btn btn-info" value="Next" />
	</fieldset>
	<fieldset>
		<h2> Step 2: Add Parameters</h2>
		<div class="form-group">
		<label for="fName">Time to run GPT-2 model for inference</label>
		<input type="text" class="form-control" placeholder="Total minutes">
	  </div>
		<input type="button" name="previous" class="previous btn btn-default" value="Previous" />
		<input type="button" name="next" class="next btn btn-info" value="Next" />
	</fieldset>
	<fieldset>
		<h2>Step 3: Run bash script on server</h2>
		<div class="form-group">
	  </div>
		<input type="button" name="previous" class="previous btn btn-default" value="Previous" />
		<input type="submit" name="submit" class="submit btn btn-success" value="Run GPT model" id="submit" />
	</fieldset>
	</form>
  </div>
</body>
</html>
<script type="text/javascript">
$(document).ready(function(){
	var current = 1,current_step,next_step,steps;
	steps = $("fieldset").length;
	$(".next").click(function(){
		current_step = $(this).parent();
		next_step = $(this).parent().next();
		next_step.show();
		current_step.hide();
		setProgressBar(++current);
	});
	$(".previous").click(function(){
		current_step = $(this).parent();
		next_step = $(this).parent().prev();
		next_step.show();
		current_step.hide();
		setProgressBar(--current);
	});
	setProgressBar(current);
	// Change progress bar action
	function setProgressBar(curStep){
		var percent = parseFloat(100 / steps) * curStep;
		percent = percent.toFixed();
		$(".progress-bar")
			.css("width",percent+"%")
			.html(percent+"%");		
	}
});
</script>