$(".app-pwd-strength").on('input', function () {
    let color_class;
    let width;

    if (this.value === "") {
        width = 0;
        color_class = "bg-transparent"
    }
    else {
        let result = zxcvbn(this.value);

        switch (result.score) {
            case 0:
                color_class = 'bg-danger';
                width = 20;
                break;
            case 1:
                color_class = 'bg-warning';
                width = 40;
                break;
            case 2:
                color_class = 'bg-warning';
                width = 60;
                break;
            case 3:
                color_class = 'bg-warning';
                width = 80;
                break;
            case 4:
                color_class = 'bg-success';
                width = 100;
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
});