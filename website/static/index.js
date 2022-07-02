function nextTest(){
var testAnswer = document.getElementById('test-answer').value;
if (testBank[currentTest- 1][0] == testAnswer) {
    window.alert("Congratulations!! Your answer is correct.");
    testScore++;
} else {
    window.alert("Incorrect!!! The correct answer is "+testBank[currentTest- 1][0] + " !");
}
currentTest+=1;
document.getElementById('test-answer').value = "";
document.getElementById("question").innerHTML = "Test: "+ currentTest + " of "+testNo;
document.getElementById("score").innerHTML = "Score: "+ testScore + " of "+testNo;

if (currentTest > testNo) {
    window.alert("Your total correct is "+ testScore + " out of "+ testNo);
    document.getElementById("question").innerHTML = "Test: "+ testNo + " of "+testNo;
    lastVocabularyID = testBank[testNo- 1][2];
    testDate = new Date();
    fetch('/log-result',{
        method: 'Post',
       body: JSON.stringify({testType: testType, lastVocabularyID: lastVocabularyID, testScore: testScore, testNo: testNo, testDate: testDate.toISOString()}) //converting timedate format to standard string format
    });
} else {
    document.getElementById("question_content").innerHTML = testBank[currentTest- 1][1];
    document.getElementById("question_1stletter").innerHTML = testBank[currentTest- 1][0][0];
    document.getElementById("question_length").innerHTML = testBank[currentTest- 1][0].length + " letters";
}
}

function deleteVocabulary(vocabularyId){
    fetch('/delete-vocabulary',{
        method: 'Post',
       body: JSON.stringify({vocabularyId: vocabularyId})
    }).then((_res) => {
       window.location.href = '/';
    });
}