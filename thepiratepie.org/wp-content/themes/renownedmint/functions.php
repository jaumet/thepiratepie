<?php
automatic_feed_links();
if (function_exists('register_sidebar')) {
	register_sidebar(array(
		'name' => 'Bottom Right',
		'id' => 'bottom-right',
		'before_widget' => '<div class="widget">',
		'after_widget' => "</div>",
		'before_title' => "<h4>",
		'after_title' => "</h4>",
		));
}

