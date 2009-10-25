<div style="clear: both;"></div> <!-- sometimes .navigation breaks the layout without this -->
</div><!-- /container -->
<div id="footer_wrapper">
	<div id="footer">
		<div id="column-1">
			<h4>Archives</h4>
			<div class="floatitems">
<?php wp_get_archives(array('type' => 'monthly', 'show_post_count' => true, 'limit' => 12, 'format' => 'custom', 'before' => "\t\t\t" . '<div class="floatitem">', 'after' => '</div>')); ?>
			</div><!-- /floatitems -->
		</div><!-- /column-1 -->
		<div id="column-2">
			<h4>Categories</h4>
			<ul class="floatitems">
<?php wp_list_categories(array('title_li' => '', 'show_count' => true, 'limit' => 12, 'style' => 'list', 'hierarchical' => false)); ?>
			</ul><!-- /floatitems -->
		</div><!-- /column-2 -->
		<div id="column-3">
			<?php if (!function_exists('dynamic_sidebar') || !dynamic_sidebar('bottom-right')) { ?>
			<h4>Site Information</h4>
			<ul id="site_info">
			<li>Content &copy; <?php echo date('Y'); ?> <a href="<?php echo get_option('home'); ?>"><?php echo bloginfo('name'); ?></a> except where otherwise noted.</li>
			<li>Powered by <a href="http://www.wordpress.org" target="_blank">WordPress</a>.<br />Theme is <a href="http://renownedmedia.com/blog/renownedmint-wordpress-theme/" target="_blank">RenownedMint</a> by <a href="http://renownedmedia.com" target="_blank">Renowned Media</a>.</li>
			</ul>
			<?php } ?>
		</div><!-- /column-3 -->






	</div><!-- /footer -->
</div><!-- /footer_wrapper -->
</div><!-- /container -->
<?php wp_footer(); ?>
</body>
</html>