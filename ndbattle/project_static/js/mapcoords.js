mapData = {
    hydro: function (item) {
        var scale = 0.0805;
        var new_x = item.x;
        var new_y = -item.y;

        item.x = new_x;
        item.y = new_y;

        item.x += 8500;
        item.y += 6600;

        item.x = item.x * scale;
        item.y = item.y * scale;
    },
    clocktower: function (item) {
        var scale = 0.0603;
        var new_x = item.x;
        var new_y = -item.y;

        item.x = new_x;
        item.y = new_y;

        item.x += 12400;
        item.y += 8000;

        item.x = item.x * scale;
        item.y = item.y * scale;
    },
    silo: function (item) {
        var scale = 0.0555;
        var new_x = item.x;
        var new_y = -item.y;

        item.x = new_x * scale;
        item.y = new_y * scale;

        item.x += 610;
        item.y += 440;

    },
    metro: function (item) {
        var scale = 0.09;
        var new_x = item.x;
        var new_y = -item.y;

        item.x = new_x;
        item.y = new_y;

        item.x += 5800;
        item.y += 4750;

        item.x = item.x * scale;
        item.y = item.y * scale;
    },
    gate: function (item) {
        var scale = 0.062;
        var new_x = item.x;
        var new_y = -item.y;

        item.x = new_x * scale;
        item.y = new_y * scale;

        item.x += 640;
        item.y += 510;
    },
    downtown: function (item) {
        var scale = 0.053;
        var new_x = item.x;
        var new_y = -item.y;

        item.x = new_x * scale;
        item.y = new_y * scale;

        item.x += 490;
        item.y += 540;

    },
    oasis: function (item) {
        var scale = 0.08;
        var new_x = item.x;
        var new_y = -item.y;

        item.x = new_x * scale;
        item.y = new_y * scale;

        item.x += 470;
        item.y += 560;
    }
};
