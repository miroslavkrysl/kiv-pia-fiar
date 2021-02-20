let gulp = require('gulp');
let clean = require('gulp-clean');
let merge = require('merge-stream');
let sass = require('gulp-sass');
let rename = require("gulp-rename");
sass.compiler = require('node-sass');

gulp.task('compile:css', function () {
    return gulp.src('resources/css/**/*.sass')
            .pipe(sass().on('error', sass.logError))
            .pipe(gulp.dest('fiar/static/css'));
});


gulp.task('compile:js', function () {
    return gulp.src('resources/js/**/*.js')
            .pipe(gulp.dest('fiar/static/js'));
});

gulp.task('compile:images', function () {
    return gulp.src('resources/images/**/*')
            .pipe(gulp.dest('fiar/static/images'));
});

gulp.task('libs', function () {
    return merge(
        // bootstrap
        gulp.src('node_modules/bootstrap/dist/css/bootstrap.min.css'),
        gulp.src('node_modules/bootstrap/dist/css/bootstrap.min.css.map'),
        gulp.src('node_modules/bootstrap/dist/js/bootstrap.bundle.min.js'),
        gulp.src('node_modules/bootstrap/dist/js/bootstrap.bundle.min.js.map'),

        // jquery
        gulp.src('node_modules/jquery/dist/jquery.min.js'),
        gulp.src('node_modules/jquery/dist/jquery.min.map'),

        // socket.io
        gulp.src('node_modules/socket.io/client-dist/socket.io.min.js'),
        gulp.src('node_modules/socket.io/client-dist/socket.io.min.js.map'),

        // password strength
        gulp.src('node_modules/zxcvbn/dist/zxcvbn.js'),
        gulp.src('node_modules/zxcvbn/dist/zxcvbn.js.map'),

        // font awesome
        gulp.src('node_modules/@fortawesome/fontawesome-free/js/all.min.js')
            .pipe(rename('font-awesome.min.js')),
    ).pipe(gulp.dest('fiar/static/lib'));
});

gulp.task('compile', gulp.parallel('compile:css', 'compile:js', 'compile:images'));

gulp.task('clean', function () {
    return gulp.src([
        'fiar/static/**/*'
    ], {read: false}).pipe(clean())
});

gulp.task('bundle', gulp.series('clean', gulp.parallel('compile', 'libs')));
