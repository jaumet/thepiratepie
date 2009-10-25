<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" <?php language_attributes(); ?>>
<meta http-equiv="Content-Type" content="<?php bloginfo('html_type'); ?>; charset=<?php bloginfo('charset'); ?>" />
<title><?php wp_title('&laquo;', true, 'right'); ?> <?php bloginfo('name'); ?></title>
<link rel="stylesheet" href="<?php bloginfo('stylesheet_url'); ?>" type="text/css" />
<link rel="pingback" href="<?php bloginfo('pingback_url'); ?>" />
<?php if ( is_singular() ) wp_enqueue_script( 'comment-reply' ); ?>
<?php wp_head(); ?>
</head>
<body <?php body_class(); ?>>
<div id="container">
	<div id="header">
		<div id="headings">
			<h1><a href="<?php echo get_option('home'); ?>/"><?php bloginfo('name'); ?></a></h1>
			<h2><?php bloginfo('description'); ?></h2>
		</div>
		<div id="movement">
			<div id="searchbox">
				<form role="search" method="get" action="<?php echo get_option('home'); ?>">
					<div id="search-input-text-wrapper"><input id="search-input-text" type="text" name="s" value="" class="input-text" /></div>
					<div id="search-input-submit-wrapper"><input id="search-input-submit" type="image" src="<?php echo get_template_directory_uri(); ?>/images/button.png" value="Search" class="input-submit" /></div>
				</form>
			</div>
			<ul id="navigation">
<?php wp_list_pages(array('title_li' => '', 'depth' => 0)); ?>
			</ul>
		</div>
	</div>