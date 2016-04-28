// Include gulp
var gulp = require('gulp');

// Include Our Plugins
var concat = require('gulp-concat');
var uglify = require('gulp-uglify');
var rename = require('gulp-rename');
var minifyCSS = require('gulp-minify-css');
var sourcemaps = require('gulp-sourcemaps');
var htmlmin = require('gulp-htmlmin');
var autoprefixer = require('gulp-autoprefixer');
var watch = require('gulp-watch');
var hb = require('gulp-hb');
var layouts = require('handlebars-layouts');
var del = require('del');
var connect = require('gulp-connect');
var notify = require('gulp-notify');

gulp.task('clean', function(cb) {
  del(['dist'], cb);
  del(['tmp'], cb);
});

// Compile home template
gulp.task('handlebars-index', function () {
    return gulp.src('./src/index.hbs')
        .pipe(hb({
            helpers: [
                './node_modules/handlebars-layouts/index.js'
            ],
            partials: './src/partials/layout.hbs'
        }))
        .pipe(rename('index.html'))
        .pipe(gulp.dest('./dist'));
});

// Compile developers template
gulp.task('handlebars-dev', function () {
    return gulp.src('./src/developers.hbs')
        .pipe(hb({
            helpers: [
                './node_modules/handlebars-layouts/index.js'
            ],
            partials: './src/partials/layout.hbs'
        }))
        .pipe(rename('developers.html'))
        .pipe(gulp.dest('./dist'));
});

// Compile relayer template
gulp.task('handlebars-relayer', function () {
    return gulp.src('./src/relayer.hbs')
        .pipe(hb({
            helpers: [
                './node_modules/handlebars-layouts/index.js'
            ],
            partials: './src/partials/layout.hbs'
        }))
        .pipe(rename('relayer.html'))
        .pipe(gulp.dest('./dist'));
});

// Compile faq template
gulp.task('handlebars-faq', function () {
    return gulp.src('./src/faq.hbs')
        .pipe(hb({
            helpers: [
                './node_modules/handlebars-layouts/index.js'
            ],
            partials: './src/partials/layout.hbs'
        }))
        .pipe(rename('faq.html'))
        .pipe(gulp.dest('./dist'));
});

// Copy all static assets
gulp.task('copy', function() {
  gulp.src('src/images/**')
    .pipe(gulp.dest('dist/images'));
  gulp.src('src/css/et-line/**')
    .pipe(gulp.dest('dist/css/et-line'));
  gulp.src('src/css/fonts/**')
    .pipe(gulp.dest('dist/css/fonts'));
});

// Minify HTML
gulp.task('minifyHTML', function() {
    return gulp.src('src/*.html', {base:'src'})
        .pipe(htmlmin({
            collapseWhitespace: true,
        }))
        .pipe(gulp.dest('dist'));
});

// Concatenate CSS
gulp.task('css', function() {
    return gulp.src([
            'src/css/bootstrap.css',
            'src/css/style.css',
            'src/css/dark.css',
            'src/css/font-icons.css',
            'src/css/et-line.css',
            'src/css/animate.css',
            'src/css/magnific-popup.css',
            'src/css/fonts.css',
            'src/css/responsive.css',
            'src/css/btcrelay.css'
            ])
        .pipe(autoprefixer({
            browsers: ['last 2 versions'],
            cascade: false
        }))
        .pipe(concat('all.css'))
        .pipe(gulp.dest('tmp'))
        .pipe(rename('all.min.css'))
        .pipe(sourcemaps.init())
        .pipe(minifyCSS())
        .pipe(sourcemaps.write())
        .pipe(gulp.dest('dist/css'))
        .pipe(notify({ message: 'CSS minification complete' }));
});


// Concatenate & Minify JS
gulp.task('scripts', function() {
    return gulp.src([
            'src/js/jquery.js',
            'src/js/plugins.js',
            'src/js/functions.js',

            'src/js/bitcoin-proof.js',
            'src/js/bignumber.js',
            'src/js/web3.min.js',
            'src/js/btcRelayAbi.js',
            'src/js/contractStatus.js',
            'src/js/testnetSampleCall.js'
        ])
        .pipe(concat('all.js'))
        .pipe(gulp.dest('tmp'))
        .pipe(rename('all.min.js'))
        .pipe(uglify())
        .pipe(gulp.dest('dist/js'));
});

// Watch Files For Changes
gulp.task('watch', function() {
    gulp.watch('src/images/*', ['copy']);
    gulp.watch('src/*.html', ['minifyHTML']);
    gulp.watch('src/css/*.css', ['css']);
    gulp.watch('src/js/*.js', ['scripts']);
});

// Run a webserver (with LiveReload)
gulp.task('connect', function() {
  connect.server({
    port: 8000,
    root: 'dist',
    livereload: true
  });
});

// Default Task
gulp.task('default', ['clean', 'handlebars-index', 'handlebars-dev',
    'handlebars-relayer', 'handlebars-faq', 'copy', 'minifyHTML', 'css', 'scripts',
    'connect', 'watch']);
