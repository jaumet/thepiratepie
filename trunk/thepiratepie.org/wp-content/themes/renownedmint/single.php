<?php get_header(); ?>
	<div id="content_wrapper">
		<div id="content">
	<?php if (have_posts()) : while (have_posts()) : the_post(); ?>
		<div class="navigation">
			<div class="alignleft"><?php previous_post_link('&laquo; %link') ?></div>
			<div class="alignright"><?php next_post_link('%link &raquo;') ?></div>
		</div>
		<div <?php post_class() ?> id="post-<?php the_ID(); ?>">
			<h2 class="post-title-single"><?php the_title(); ?></h2>
			<div class="post-date-single"><?php the_time('M jS, Y') ?> at <?php the_time() ?></div>
			<div class="entry">
				<?php the_content('<p class="serif">Read the rest of this entry &raquo;</p>'); ?>
				<?php wp_link_pages(array('before' => '<p><strong>Pages:</strong> ', 'after' => '</p>', 'next_or_number' => 'number')); ?>
				<?php the_tags( '<p>Tags: ', ', ', '</p>'); ?>
				<p class="postmetadata alt">
					<small>
						In <?php the_category(', ') ?>.
						<?php if ( comments_open() && pings_open() ) { ?>
							You can <a href="#respond">leave a response</a>, or <a href="<?php trackback_url(); ?>" rel="trackback">trackback</a> from your site.
						<?php } elseif ( !comments_open() && pings_open() ) { ?>
							Responses are currently closed, but you can <a href="<?php trackback_url(); ?>" rel="trackback">trackback</a> from your site.
						<?php } elseif ( comments_open() && !pings_open() ) { ?>
							You can skip to the end and leave a <a href="#respond">response</a>. Pinging is currently not allowed.
						<?php } elseif ( !comments_open() && !pings_open() ) { ?>
							Both comments and pings are currently closed.
						<?php } edit_post_link('Edit this entry','','.'); ?>
					</small>
				</p>
			</div>
		</div>
	<?php comments_template(); ?>
	<?php endwhile; else: ?>
		<p>Sorry, no posts matched your criteria.</p>
<?php endif; ?>
		</div>
	</div>
<?php get_footer(); ?>
