document.addEventListener("keydown", function (event) {
    if (event.key.toLowerCase() == "enter") {
        // console.log("Key pressed:", event.key);
        getSelectedGame()

    }
});

// ----- initiallizing the dropdown
let gamesDropDown = $('.ui.games')
    .dropdown({
        clearable: true,
        // direction: 'downward'
        forceSelection: false,
        onChange: function (item) {
            console.log(item);
            // let submitGameButton = document.getElementById("submitGameButton")
            if (item.trim()) {
                // submitGameButton.classList.remove('disabled')
            } else {
                // submitGameButton.classList.add('disabled')
            }

        }
    })



fillGamesDropDown()
function fillGamesDropDown() {

    let menu = document.querySelector(".menu");
    $.ajax({
        url: "get_list_of_games",
        type: 'GET',
        dataType: 'json',
        beforeSend: function () { },
        success: function (games) {
            games.map((item) => {

                let newItem = document.createElement("div");

                newItem.setAttribute("class", "item");
                newItem.setAttribute("data-value", item.id + ":" + item.gameName + "");

                // newItem.innerHTML = '<i class="pk flag"></i>' + item.gameName + '';
                newItem.innerHTML = item.gameName;

                menu.appendChild(newItem);
            })
        }

    })
}

function getSelectedGame() {

    let selectedGame = gamesDropDown.dropdown('get value');

    let gameObj = selectedGame.split(":")

    let gameId = gameObj[0]
    // let gameName = gameObj[1]

    if (gameId) {
        //redirect user to url
        window.location.href = "/game/" + gameId;
    }
}


