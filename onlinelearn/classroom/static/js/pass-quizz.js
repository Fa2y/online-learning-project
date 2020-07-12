//for loading css in already made head
var newStyle = document.createElement("link");
newStyle.rel = "stylesheet";
newStyle.href = "../static/css/style.css";
document.getElementsByTagName("head")[0].appendChild(newStyle);
let data = JSON.parse(document.getElementById('data').value);
document.querySelector("span.name").innerHTML = data['quizzname']
document.querySelector("p.author").innerHTML = "author " + data['author']
//  [
//   {
//     id: 1,
//     question: "What is the full form of RAM ?",
//     answer: "Random Access Memory",
//     options: [
//       "Random Access Memory",
//       "Randomely Access Memory",
//       "Run Aceapt Memory",
//       "None of these"
//     ]
//   },
//   {
//     id: 2,
//     question: "What is the full form of CPU?",
//     answer: "Central Processing Unit",
//     options: [
//       "Central Program Unit",
//       "Central Processing Unit",
//       "Central Preload Unit",
//       "None of these"
//     ]
//   },
//   {
//     id: 3,
//     question: "What is the full form of E-mail",
//     answer: "Electronic Mail",
//     options: [
//       "Electronic Mail",
//       "Electric Mail",
//       "Engine Mail",
//       "None of these"
//     ]
//   }
// ];

let question_count = 0;
let points = 0;
let answers = {};
window.onload = function() {
  show(question_count);
  progressBar(question_count+1,data['questions'].length);
};

function next() {
  
  answers["answer"+String(question_count)] = []
  let user_answers = document.querySelectorAll("li.option.active");
  if (user_answers.length == 0 ){
    answers["answer"+String(question_count)][0] = ""
  }
  for (let i = 0; i < user_answers.length; i++) {
    answers["answer"+String(question_count)][i] = user_answers[i].innerHTML;
  }
  // if the question is last then redirect to final page
  if (question_count == data['questions'].length - 1) {
    var xhr = new XMLHttpRequest();
    answers["csrfmiddlewaretoken"] = $("[name='csrfmiddlewaretoken']").attr("value")
  
    $.ajax({url : document.location,type: 'POST', data: answers, xhr : function (){ return xhr;},success : function(response){document.location.href = xhr.responseURL;}});
    return;
  }
  if (question_count == data['questions'].length - 2) {
    btn = $(".btn-next");
    btn.removeClass("btn-next");
    btn.addClass("btn-submit");
    btn.attr("title","Submit Answers");
    btn.html( '<svg width="2.5em" height="2.5em" viewBox="0 0 16 16" class="bi bi-check2-all" fill="currentColor" xmlns="http://www.w3.org/2000/svg">\
  <path fill-rule="evenodd" d="M12.354 3.646a.5.5 0 0 1 0 .708l-7 7a.5.5 0 0 1-.708 0l-3.5-3.5a.5.5 0 1 1 .708-.708L5 10.293l6.646-6.647a.5.5 0 0 1 .708 0z"/>\
  <path d="M6.25 8.043l-.896-.897a.5.5 0 1 0-.708.708l.897.896.707-.707zm1 2.414l.896.897a.5.5 0 0 0 .708 0l7-7a.5.5 0 0 0-.708-.708L8.5 10.293l-.543-.543-.707.707z"/>\
</svg>' );
    btn.on('click',function () {
      btn.html('<span class="spinner-border" role="status" aria-hidden="true"></span>');  
    })
  }
  console.log(question_count);

  // // check if the answer is right or wrong
  // if (user_answer == questions[question_count].answer) {
  //   points += 10;
  //   sessionStorage.setItem("points", points);
  // }
  // console.log(points);

  question_count++;
  progressBar(question_count+1,data['questions'].length);
  show(question_count);
}

function show(count) {
  let question = document.getElementById("questions");
  let options = data['questions'][count].options;

  question.innerHTML = `
  <h2>Q${count + 1}. ${data['questions'][count]['question']}</h2>
   <ul class="option_group">
</ul> 
  `;
  opt_grp = $('.option_group');
  for (let i = 0; i<options.length; i++){
    opt_grp.append($("<li class='option'>"+options[i]+"</li>"));
  }
  toggleActive();
}

function toggleActive() {
  let option = document.querySelectorAll("li.option");
  for (let i = 0; i < option.length; i++) {
    option[i].onclick = function() {
      // for (let i = 0; i < option.length; i++) {
      //   if (option[i].classList.contains("active")) {
      //     option[i].classList.remove("active");
      //   }
      // }
      if (option[i].classList.contains("active")){
          option[i].classList.remove("active");

      }else{
      option[i].classList.add("active");
    }
    };
  }
}
function progressBar(count,total){
  pb = $('.progress-bar');
  pb.width((count*800)/total);
}
