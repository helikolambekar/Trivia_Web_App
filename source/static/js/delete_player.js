function deletePlayer(playerId) {
    fetch('/admin/delete-player', {
        method: "POST",
        body: JSON.stringify({
            playerId: playerId
        }),
    }).then((_res) => {
        window.location.href = "/admin/players";
    })
}