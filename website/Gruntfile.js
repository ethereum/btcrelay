'use strict';

module.exports = function(grunt) {
	require('load-grunt-tasks')(grunt);

	// src paths
	var SRC_DIR = 'src/';
	var SRC_DIR_JS = SRC_DIR + 'js/';
	var SRC_DIR_LESS = SRC_DIR + 'less/';
	var SRC_DIR_PUG = SRC_DIR + 'views/';
	var SRC_DIR_IMAGES = SRC_DIR + 'images/';
	var SRC_DIR_FONTS = SRC_DIR + 'fonts/';
	var SRC_FILES_JS = SRC_DIR_JS + '*.js';
	var SRC_FILE_LESS = SRC_DIR_LESS + 'style.less';
	var SRC_FILES_LESS = SRC_DIR_LESS + '*.less';
	var SRC_FILES_PUG = SRC_DIR_PUG + '*.pug';
	var WATCH_FILES_PUG = SRC_DIR_PUG + '**/*.pug';
	var SRC_FILES_IMAGES = SRC_DIR_IMAGES + '**';
	var SRC_FILES_FONTS = SRC_DIR_FONTS + '**';

	// bower dependencies
	var SRC_BOWER_DIR = 'bower_components/';
	var SRC_JQUERY_DIR = 'jquery/dist/';
	var SRC_JQUERY_JS_DIR = SRC_BOWER_DIR + SRC_JQUERY_DIR;
	var SRC_JQUERY_JS_FILE = 'jquery.min.js';
	var SRC_BOOTSTRAP_DIR = 'bootstrap/dist/';
	var SRC_BOOTSTRAP_JS_DIR = SRC_BOWER_DIR + SRC_BOOTSTRAP_DIR + 'js/';
	var SRC_BOOTSTRAP_JS_FILE = 'bootstrap.min.js';
	var SRC_BOOTSTRAP_FONTS_DIR = SRC_BOWER_DIR + SRC_BOOTSTRAP_DIR + 'fonts/';

	// build paths
	var BUILD_DIR = 'dist/';
	var BUILD_DIR_JS = BUILD_DIR + 'js/';
	var BUILD_DIR_CSS = BUILD_DIR + 'css/';
	var BUILD_DIR_IMAGES = BUILD_DIR + 'images/';
	var BUILD_DIR_FONTS = BUILD_DIR + 'fonts/';
	var BUILD_FILE_JS = BUILD_DIR_JS + 'app.js';
	var BUILD_FILE_CSS = BUILD_DIR_CSS + 'style.css';

	var AP_BROWSERS = [
		'Android 2.3',
		'Android >= 4',
		'Chrome >= 20',
		'Firefox >= 24', // Firefox 24 is the latest ESR
		'Explorer >= 8',
		'iOS >= 6',
		'Opera >= 12',
		'Safari >= 6'
	];

	var PUG_FILE_CFG =  [{
		expand: true,
		cwd: SRC_DIR_PUG,
		src: ['*.pug'],
		dest: BUILD_DIR,
		ext: '.html'
	}];

	// object to represent the type of environment we are running in.
	// eg. production or development
	var EnvType = {
		prod: 'production',
		dev: 'development'
	};

	grunt.initConfig({
		pkg: grunt.file.readJSON('package.json'),

		// wipe the build directory clean
		clean: {
			build: {
				src: [BUILD_DIR]
			},
			images: {
				src: [BUILD_DIR_IMAGES]
			},
			fonts: {
				src: [BUILD_DIR_FONTS]
			},
			scripts: {
				src: [BUILD_DIR_JS + '*.js', ['!' + BUILD_FILE_JS, '!' + SRC_BOOTSTRAP_JS_FILE, '!' + SRC_JQUERY_JS_FILE]]
			}
		},

		// copy files into dist directory
		copy: {
			build: {
				files: [{
					cwd: SRC_DIR,
					src: ['**', '!**/less/**', '!**/views/**'],
					dest: BUILD_DIR,
					expand: true
				},
				{
					cwd: SRC_BOOTSTRAP_FONTS_DIR,
					src: ['**'],
					dest: BUILD_DIR_FONTS,
					expand: true
				}]
			},
			vendor: {
				files: [{
					cwd: SRC_BOOTSTRAP_JS_DIR,
					src: SRC_BOOTSTRAP_JS_FILE,
					dest: BUILD_DIR_JS,
					expand: true
				},
				{
					cwd: SRC_JQUERY_JS_DIR,
					src: SRC_JQUERY_JS_FILE,
					dest: BUILD_DIR_JS,
					expand: true
				}]
			}
		},

		// Configure the less compilation for both dev and prod
		less: {
			development: {
				files: {
					"dist/css/style.css": SRC_FILE_LESS
				}
			},
			production: {
				options: {
					// minify css in prod mode
					cleancss: true,
				},
				files: {
					"dist/css/style.css": SRC_FILE_LESS
				}
			}
		},

		// configure autoprefixing for compiled output css
		autoprefixer: {
			options: {
				browsers: AP_BROWSERS
			},
			build: {
				expand: true,
				cwd: BUILD_DIR,
				src: ['css/*.css'],
				dest: BUILD_DIR
			}
		},

		// configure concatenation for the js: for dev mode.
		// this task will only concat files. useful for when in development
		// and debugging as the file will be readable.
		concat: {
			dist: {
				// if some scripts depend upon eachother,
				// make sure to list them here in order
				// rather than just using the '*' wildcard.
				src: [SRC_DIR_JS + '*.js'],
				dest: BUILD_FILE_JS
			}
		},

		// configure minification for the js: for prod mode.
		// this task both concatenates and minifies the files.
		uglify: {
			build: {
				options: {
					banner: '/*! <%= pkg.name %>' +
					'<%= grunt.template.today("dd-mm-yyyy") %> */\n',
					mangle: false
				},
				files: {
					"dist/js/app.js": [BUILD_DIR_JS + '*.js']
				}
			}
		},

		// configure the pug template file compilation
		pug: {
			development: {
				options: {
					pretty: true,
					debug: true,
					data: {
					}
				},
				files: PUG_FILE_CFG
			},

			production: {
				options: {
					debug: false,
					data: {
					}
				},
				files: PUG_FILE_CFG
			}
		},

		// grunt-express will serve the files from the folders listed in `bases`
		// on specified `port` and `hostname`
		express: {
			all: {
				options: {
					port: 3001,
					hostname: "0.0.0.0",
					bases: [BUILD_DIR],
					livereload: true
				}
			}
		},

		// configure grunt-watch to monitor the projects files
		// and perform each specific file type build task.
		watch: {
			images: {
				options: { livereload: false },
				files: [SRC_FILES_IMAGES],
				tasks: ['clean:images', 'copy']
			},

			fonts: {
				options: { livereload: false },
				files: [SRC_FILES_FONTS],
				tasks: ['clean:fonts', 'copy']
			},

			scripts: {
				options: { livereload: false },
				files: [SRC_FILES_JS],
				tasks: ['concat']
			},

			stylesless: {
				options: { livereload: true },
				files: [SRC_FILES_LESS],
				tasks: ['less:development', 'autoprefixer']
			},

			pug: {
				options: { livereload: true },
				files: [WATCH_FILES_PUG],
				tasks: ['pug:development']
			}
		},

		// grunt-open will open your browser at the project's URL
		open: {
			all: {
				// Gets the port from the connect configuration
				path: 'http://localhost:<%= express.all.options.port%>'
			}
		}
	});

		/**
	 * Utility function to register the stylesheets task to grunt.
	 * @param  {[type]} mode  [the mode, either dev, or production]
	 */
	var registerStyleSheetsTask = function(mode) {
		grunt.registerTask('stylesheets:' + mode,
			'Compiles the stylesheets for development mode',
			['less:' + mode, 'autoprefixer']
		);
	};

	/**
	 * Utility function to register the scripts task to grunt.
	 * @param  {[type]} mode  [the mode, either dev, or production]
	 */
	var registerScriptsTask = function(mode) {
		// if we are running in dev mode, only concat the scripts
		// otherwise minify them also
		var scriptTask = (mode === EnvType.dev) ? 'concat' : 'uglify';

		grunt.registerTask('scripts:' + mode,
			'Compiles the javascript files in ' + mode + ' mode',
			[ scriptTask, 'copy:vendor', 'clean:scripts']
		);
	};

	/**
	 * Utility function to register the build task to grunt.
	 * @param  {[type]} mode  [the mode, either dev, or production]
	 */
	var registerBuildTask = function(mode) {
		grunt.registerTask('build:' + mode,
			'Compiles all of the assets and copies them' +
			' to th build directory',
			['clean:build', 'copy:build', 'stylesheets:' + mode, 'scripts:' + mode,
				'copy:vendor', 'pug:' + mode]
		);
	};

	/**
	 * Utility function to register the server task to grunt.
	 * @param  {[type]} mode  [the mode, either dev, or production]
	 */
	var registerServerTask = function(mode) {
		var tasks = ['express', 'open'];

		// if we are running in development mode, run the watch task
		if (mode === EnvType.dev) {
			tasks.push('watch');
		} else if (mode === EnvType.prod) {
			tasks.push('express-keepalive');
		}

		grunt.registerTask('server:' + mode,
			'Begins the express server and opens it in a browser' +
			'constantly watching for changes',
			tasks
		);
	};

	/**
	 * Utility function to register the main task to grunt.
	 * @param  {[type]} mode  [the mode, either dev, or production]
	 */
	var registerMainTask = function(mode) {
		grunt.registerTask(mode,
			'Watches the project for changes' +
			'automatically builds them and runs a server',
			['build:' + mode, 'server:' + mode]
		);
	};

	// register all the tasks for both development and production
	registerStyleSheetsTask(EnvType.dev);
	registerStyleSheetsTask(EnvType.prod);
	registerScriptsTask(EnvType.dev);
	registerScriptsTask(EnvType.prod);
	registerBuildTask(EnvType.dev);
	registerBuildTask(EnvType.prod);
	registerServerTask(EnvType.dev);
	registerServerTask(EnvType.prod);
	registerMainTask(EnvType.dev);
	registerMainTask(EnvType.prod);

	// register development mode as the main task
	grunt.registerTask('default', 'Default task: development', 'development');

	// grunt.registerTask('build',   'default');
};