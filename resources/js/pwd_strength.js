$(".app-pwd-strength").on('input', function () {
    let color_class;
    let width;
    let text;

    if (this.value === "") {
        width = 0;
        color_class = "bg-transparent"
        text = ""
    }
    else {
        let result = zxcvbn(this.value);

        switch (result.score) {
            case 0:
                color_class = 'bg-danger';
                width = 20;
                text = "very weak"
                break;
            case 1:
                color_class = 'bg-warning';
                width = 40;
                text = "weak"
                break;
            case 2:
                color_class = 'bg-warning';
                width = 60;
                text = "medium"
                break;
            case 3:
                color_class = 'bg-warning';
                width = 80;
                text = "strong"
                break;
            case 4:
                color_class = 'bg-success';
                width = 100;
                text = "very strong"
                break;
        }
    }

    let bar_id = "#" + $(this).attr("data-strength-bar");

    console.log(color_class)
    console.log(width)

    $(bar_id).css('width', width+'%').attr('aria-valuenow', width);
    $(bar_id).removeClass(
        ['bg-danger',
        'bg-warning',
        'bg-success',
        'bg-transparent']
    )
    $(bar_id).addClass(color_class);
    $(bar_id).html(text);
});