const notificationsList = document.getElementById("notifications-list");
const notificationsButton = document.getElementById("notifications-show-more");
const userId = document.getElementsByClassName("user-id")[0].textContent.replace("@", "");

let lastPoke = null;

function loadNotifications() {
    fetch("/api/pokes?limit=10&id=" + userId + "&before=" + lastPoke).then(response => response.json()).then(notifications => {   
        if(notifications.length == 0) {
            notificationsButton.remove();
            return;
        }
        let html = "";
        notifications.forEach(notification => {
            let time = notification["created"].substring(0, 16)
            html+= `
            <div class="user-item button" onclick="location.href = '/@${notification["poker"]}';" style="margin: 0 -16px;">
                <span class="material-icons">notifications</span>
                <div>
                    <span class="user-name">You were poked by @${notification["poker"]}</span>
                    <span class="user-id">${time}</span>
                </div>
            </div>`;
        });
        notificationsList.innerHTML += html;
        lastPoke = notifications[notifications.length - 1]["created"];
    });
}

notificationsButton.addEventListener("click", loadNotifications);
loadNotifications();
