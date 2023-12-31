function GetURLParameter(sParam) {
  var sPageURL = window.location.search.substring(1);
  var sURLVariables = sPageURL.split("&");
  for (var i = 0; i < sURLVariables.length; i++) {
    var sParameterName = sURLVariables[i].split("=");
    if (sParameterName[0] == sParam) {
      return sParameterName[1];
    }
  }
}

function saveData(name, data) {
  var xhr = new XMLHttpRequest();
  xhr.open("POST", "write_data.php"); // 'write_data.php' is the path to the php file described above.
  xhr.setRequestHeader("Content-Type", "application/json");
  xhr.send(JSON.stringify({ filename: name, filedata: data }));
}

function to_string(a) {
  return `sounds/${a}_ms.ogg`;
}

function to_dict(a) {
  return { stimulus: a };
}

sona_subject_id = GetURLParameter("subject");
if (!subject_id) {
  var subject_id = jsPsych.randomization.randomID(15);
}
console.log(sona_subject_id);

jsPsych.data.addProperties({
  subject: subject_id,
  sona: sona_subject_id,
});

var durations = [ 180, 200, 210, 215, 220, 225, 230, 235, 240, 245, 250, 255,
    260, 265, 270, 275, 280, 285, 290, 295, 300, 305, 310, 315, 320, 325, 330,
    335, 340, 345, 350, 355, 360, 365, 370, 375, 380, 385, 390, 400, 420, ];
var weights = [ 0.004879201857918277, 0.005959470606881607, 0.0072064874336218,
    0.008627731882651153, 0.010226492456397803, 0.012000900069698558,
    0.013943056644536028, 0.01603833273419196, 0.01826490853890219,
    0.020593626871997478, 0.0229882140684233, 0.025405905646918903,
    0.027798488613099647, 0.030113743215480444, 0.03229723596679143,
    0.03429438550193839, 0.03605269624616479, 0.03752403469169379,
    0.03866681168028493, 0.039447933090788895, 0.039844391409476404,
    0.039844391409476404, 0.039447933090788895, 0.03866681168028493,
    0.03752403469169379, 0.03605269624616479, 0.03429438550193839,
    0.03229723596679143, 0.030113743215480444, 0.027798488613099647,
    0.025405905646918903, 0.0229882140684233, 0.020593626871997478,
    0.01826490853890219, 0.01603833273419196, 0.013943056644536028,
    0.012000900069698558, 0.010226492456397803, 0.008627731882651153,
    0.0072064874336218, 0.005959470606881607, ];

var n_trials = 25;
var fns = durations.map(to_string);
var test_stimuli = fns.map(to_dict);

console.log(test_stimuli);

var fixation = {
  type: "html-keyboard-response",
  stimulus: '<div style="font-size:60px;">+</div>',
  choices: jsPsych.NO_KEYS,
  trial_duration: 1000,
};

var fin = {
  type: "html-keyboard-response",
  stimulus: "Finished! Thank you :-)",
  choices: jsPsych.NO_KEYS,
};

var trial_const = {
  type: "audio-keyboard-response",
  stimulus: "sounds/300_ms.ogg",
  choices: jsPsych.NO_KEYS,
  trial_ends_after_audio: true,
};

var trial = {
  type: "audio-button-response",
  stimulus: jsPsych.timelineVariable("stimulus"),
  choices: ["shorter", "longer"],
  prompt: "<p>Was the last beep shorter or longer than the one before?</p>",
  response_ends_trial: true,
};

var test_procedure = {
  timeline: [trial_const, fixation, trial, fixation],
  timeline_variables: test_stimuli,
  on_finish: function () {
    saveData(
      `experiment_data_${sona_subject_id}_${subject_id}`,
      jsPsych.data.get().csv()
    );
    var curr_progress_bar_value = jsPsych.getProgressBarCompleted();
    jsPsych.setProgressBar(curr_progress_bar_value + 1 / n_trials / 4);
  },
  sample: {
    type: "without-replacement",
    size: n_trials,
    weights: weights,
  },
  randomize_order: true,
};

jsPsych.init({
  timeline: [test_procedure, fin],
  show_progress_bar: true,
  auto_update_progress_bar: false,
});
