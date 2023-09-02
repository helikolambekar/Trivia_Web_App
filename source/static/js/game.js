$(document).ready(function () {

    initGameVariables();

    //read and keep answer location
    var answer_location;
    //read and keep user selection
    var user_selection = [];

    // for 50/50 function
    var fifty_fifty_left = fifty_fifty_chances;

    // for skip question function
    var skipleft = MaxSkip;

    // for timer function and score function
    var timerpower = true; //determines whether timer is active or not

    //Make Add score to Leader board form appear
    $('#submitScore').click(function () {
        console.log('clicked!');
        $('#cover-caption').slideToggle("slow");
    });
    $('#submitScore').hide()

    var opt = $('.option');
    // Set up the initial option color
    opt.css('color', 'black');
    opt.css('background-color', 'white').css('color', 'black');
    // clicking on any of the options will return value to user_selection
    opt.on('click', Selection);
    // click option will change the option background color
    opt.on('click', ChangeSelectedOptionColor);

    //Submit button, Check if selection is correct
    var sub = $('#submit');
    sub.on('click', Submit);

    //Next button, for new question
    var next = $('#next');
    next.on('click', DisplayNewQuestion);
    next.hide();

    // Skip question function
    $('#SkipQuestion').click(function () {
        if (skipleft <= 0) {
            console.log('No more skips!');
            return false;
        }

        //Get skip question data from backend
        ajaxSkipQuestion()

        document.querySelector('#SkipQuestion').textContent = 'Skip Question (' + skipleft + ')';
        console.log('Skipped!');
        DisplayNewQuestion();
        if (skipleft <= 0) {
            document.getElementById('SkipQuestion').disabled = true;
        }
        ;
    });

    function ajaxSkipQuestion() {
        $.ajax({
            dataType: 'json',
            type: 'GET',
            url: '/game/skip_question',
            data: {"GameID": localStorage.getItem("gameID")},
            async: false,
            success: function (data) {
                console.log(typeof data);
                console.log(data);

                skipleft = data;
            }
        });
    }

    // fifty fifty lifeline function
    $('#FiftyFifty').click(function () {
        ajaxFiftyFifty();
        $('#FiftyFifty').text("50 / 50 (" + fifty_fifty_left + ")");
        if (removeable_option1 == 1) {
            $('#option_1').hide()
        } else if (removeable_option1 == 2) {
            $('#option_2').hide()
        } else if (removeable_option1 == 3) {
            $('#option_3').hide()
        } else if (removeable_option1 == 4) {
            $('#option_4').hide()
        }
        if (removeable_option2 == 1) {
            $('#option_1').hide()
        } else if (removeable_option2 == 2) {
            $('#option_2').hide()
        } else if (removeable_option2 == 3) {
            $('#option_3').hide()
        } else if (removeable_option2 == 4) {
            $('#option_4').hide()
        }
        document.getElementById('FiftyFifty').disabled = true;
    });

    function ajaxFiftyFifty() {
        $.ajax({
            dataType: 'json',
            type: 'GET',
            url: '/game/fifty_fifty',
            data: {"GameID": localStorage.getItem("gameID")},
            async: false,
            success: function (data) {
                // Log data on front end
                console.log(typeof data);
                console.log(data);

                //initialize the variables from the ajax data
                removeable_option1 = data[0]['first_option'];
                removeable_option2 = data[1]['second_option'];
                fifty_fifty_left = data[2]['attempt'];
            }
        });
    }


    // Timer - will be implementing this on the back end last
    var Timer = setInterval(function () {
        if (timerpower == true) {

            if (timeleft < 0) {

                document.getElementById("Timer").innerHTML = "Finished";
                alert("Timeout!");
                user_selection[0] = 5;
                Submit()
                timeleft = timer;

            } else {
                document.getElementById("Timer").innerHTML = timeleft + " seconds";
            }
            timeleft -= 1;
        }
    }, 1000);

    //get initial game data via ajax request similar to get question data - This also resets the game data to the default state
    function initGameVariables() {
        $.ajax({
            dataType: 'json',
            type: 'GET',
            url: '/game/settings',
            data: {"GameID": localStorage.getItem("gameID")},
            async: false,
            success: function (data) {
                //initialize the variables from the ajax data
                attempt_counter = data[0]['Lives'];
                MaxSkip = data[3]['Number Question Skips'];
                timer = data[1]['Question Time'];
                player_score = data[2]['Score'];
                timeleft = timer;
                fifty_fifty_chances = data[9]["Fifth Fifty Attempt"];

                //replace front end ui with NEW data from server
                $('#question').text(data[4]['Question']);
                option1 = $('#option_1').text("A: " + data[5]['Option_1']);
                option2 = $('#option_2').text("B: " + data[6]['Option_2']);
                option3 = $('#option_3').text("C: " + data[7]['Option_3']);
                option4 = $('#option_4').text("D: " + data[8]['Option_4']);
            }
        });
    }

    //get user selection when player click the option
    function Selection() {
        user_selection = $(this);
        console.log(user_selection[0] + 'clicked!');
    }

    // change the player selected option's color
    function ChangeSelectedOptionColor() {
        opt.css('background-color', 'white').css('color', 'black');
        $(user_selection).css('background-color', 'grey').css('color', 'white');
    }

    // All of the functionality attached to the player clicking the 'Submit' button
    function Submit() {
        //Get the answer location for the last question loaded into the game object
        ajaxAnswerLocation()

        // check user selection is empty or not
        if (user_selection[0] == undefined) {

            alert("Please select an option!");


        } else {

            // all the function turn on or off are in the SettingForSubmit
            SettingForSubmitButton();

            // if else function for check if player answer right or wrong
            if (user_selection[0] == CheckAnswer()) {


                // change answer color to green
                $(CheckAnswer()).css('background-color', 'green').css('color', 'white');

                //update the score
                ajaxUpdateScore()
                $('#Counter').html(player_score);

            } else {
                // change user_selection color to red, and answer to green
                $(user_selection).css('color', 'red');
                $(CheckAnswer()).css('background-color', 'green').css('color', 'white');

                //Remove one of the remaining lives and update the lives display
                ajaxRemoveLife()
                UpdateLives();
            }

            // When no more attempts are left run through the end of game logic
            if (attempt_counter <= 0) {
                //Alert the player the game is over
                gameOver();
            }
        }
    }

    function ajaxAnswerLocation() {
        $.ajax({
            dataType: 'json',
            type: 'GET',
            url: '/game/answer',
            data: {"GameID": localStorage.getItem("gameID")},
            async: false,
            success: function (data) {
                // Log data on front end
                console.log(typeof data);
                console.log(data);

                //update the answer location
                answer_location = data[0]['Answer_Location'];
            }
        });
    }

    function ajaxUpdateScore() {
        $.ajax({
            dataType: 'json',
            type: 'GET',
            url: '/game/update_score',
            data: {"GameID": localStorage.getItem("gameID")},
            async: false,
            success: function (data) {
                // Log data on front end
                console.log(typeof data);
                console.log(data);

                //update the answer location
                player_score = data;
            }
        });
    }

    function ajaxRemoveLife() {
        $.ajax({
            dataType: 'json',
            type: 'GET',
            url: '/game/removelife',
            data: {"GameID": localStorage.getItem("gameID")},
            async: false,
            success: function (data) {
                // Log data on front end
                console.log(typeof data);
                console.log(data);

                //update the answer location
                attempt_counter = data;
            }
        });
    }

    // All of the functionality attached to the player clicking the 'Next Question' button
    function DisplayNewQuestion() {

        // Set all button back to default setting
        SettingForDisplayNewQuestion();

        //TODO We need to implement a notification which displays when the player has cycled through the questions available.

        $.ajax({
            dataType: 'json',
            type: 'GET',
            url: '/question/',
            data: {"GameID": localStorage.getItem("gameID")},
            success: function (data) {
                // Log data on front end
                console.log(typeof data);
                console.log(data);

                //replace front end ui with NEW data from server
                $('#question').text(data[0]['Question']);
                option1 = $('#option_1').text("A: " + data[1]['Option_1']);
                option2 = $('#option_2').text("B: " + data[2]['Option_2']);
                option3 = $('#option_3').text("C: " + data[3]['Option_3']);
                option4 = $('#option_4').text("D: " + data[4]['Option_4']);
            }
        });

    }

    // function for checking which option is the answer
    function CheckAnswer() {
        //answer_location is getting from DisplayNewQuestion(), and the value is a int

        q_answer = window['option_' + answer_location];

        // the return value is a HTML <div>...</div>,
        // something like: <div class="col-md-5 text-center option btn btn-outline-secondary" id="option_1" style="color: green;">B: Baker Street</div>
        return q_answer;
    }

    // Display remaining lives
    function UpdateLives() {
        $(".stats").html('<h4>' + 'LIVES: <span style="color:red"> ' + attempt_counter + '/3' + '</span></h4>');
    }

    // Here to change the button and related function activate or deactivate for Submit() function
    function SettingForSubmitButton() {
        // turn off the selected option color change function,
        // when user submit their answer, selected option no longer available to change color
        opt.off('click', ChangeSelectedOptionColor);

        //pause the timer
        timerpower = false;

        //turn off the skip question button after question submission
        if (skipleft > 0) {
            document.getElementById('SkipQuestion').disabled = true;
            document.querySelector('#SkipQuestion').textContent = 'Skip Question (' + skipleft + ')';
        }
        ;

        //turn off the 50/50 button after question submission
        if (fifty_fifty_left > 0) {
            document.getElementById('FiftyFifty').disabled = true;
            document.querySelector('#FiftyFifty').textContent = '50 / 50 (' + fifty_fifty_left + ')';
        }
        ;

        // hide Submit button, user already submitted once
        sub.hide();

        // show next button
        next.show();
    }

    // Here to change the button and related function activate or deactivate for DisplayNewQuestion() function
    function SettingForDisplayNewQuestion() {
        //reset the answer location variable to 0, it will be set to the correct location upon clicking submit
        answer_location = 0

        //turn on all options
        $('#option_1').show();
        $('#option_2').show();
        $('#option_3').show();
        $('#option_4').show();

        // turn on the color change function for selected option
        opt.on('click', ChangeSelectedOptionColor);

        // show submit button, new question, user can do submit
        sub.show();

        // turn off and hide next button, user cannot go next before submit
        next.hide();

        // turn on and reset the timer
        timerpower = true;
        timeleft = timer;

        // enable the skip question button if skips remain
        if (skipleft > 0) {
            document.getElementById('SkipQuestion').disabled = false;
        }
        ;

        // enable the 50/50 button if 50/50 chances remain
        if (fifty_fifty_left > 0) {
            document.getElementById('FiftyFifty').disabled = false;
        }
        ;

        // set all option colors back to default
        opt.css('color', 'black');
        opt.css('background-color', 'white').css('color', 'black');

        // refresh user selection to an empty list
        user_selection = [];
    }


    function gameOver() {
        alert("Game over!");
        $('#Score').val(player_score);
        $('#Score_No_Login').html(player_score);
        $('#next').detach();
        $('#submit').detach();
        $('input[name="score"]').val(player_score);
        $('#cover-caption').slideToggle("slow");
        $('#main-container').hide();
        $('#optionboard').hide();
        $('#quit').hide();
        $('#SkipQuestion').hide();
    }

});