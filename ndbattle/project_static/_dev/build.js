({
	baseUrl: '../js/',
	paths: {
		"jquery": '../_dev/jquery-2.2.3.min'
	},
	shim: {
		"base": ['jquery']
	},
	name: '../_dev/almond',
	include: [
		"jquery",
		"base"
	],
	out: '../js/common.js',
	logLevel: 0,
	preserveLicenseComments: false
})
