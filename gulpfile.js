let gulp = require('gulp');
let clean = require('gulp-clean');
let merge = require('merge-stream');
let sass = require('gulp-sass');
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
        gulp.src('node_modules/bootstrap/dist/css/bootstrap.min.css'),
        gulp.src('node_modules/bootstrap/dist/css/bootstrap.min.css.map'),
        gulp.src('node_modules/bootstrap/dist/js/bootstrap.bundle.js'),
        gulp.src('node_modules/jquery/dist/jquery.min.js'),
        gulp.src('node_modules/sockjs-client/dist/sockjs.min.js'),
    ).pipe(gulp.dest('fiar/static/lib'));
});

gulp.task('compile', gulp.parallel('compile:css', 'compile:js', 'compile:images'));

gulp.task('clean', function () {
    return gulp.src([
        'fiar/static/**/*'
    ], {read: false}).pipe(clean())
});

gulp.task('bundle', gulp.series('clean', gulp.parallel('compile', 'libs')));
