
!function($){
	"use strict"
	
	$(document).ready(function(){
		$('.up-btn').on('click',function(){
			$('body').animate({
				scrollTop : 0
			},500);
		});
		$(window).on('scroll',function(){
			var scrollY = $(window).scrollTop();
			if(scrollY > 40){
				$('.switch').addClass('scroll');
				$('.up-btn').fadeIn();
			}else{
				$('.switch').removeClass('scroll');
				$('.up-btn').fadeOut();
			}
		});
		
		
		
		$.fn.nameAutocomplete = function(options){
			var self = this;
			var $self = $(this);			
		 
			
			$self.wrapInner('<div class="friends-names well" />');		
			$self.find('.friends-names').wrapInner('<div class="friends-names-overlay" />');
			$self.prepend('<div class="result-box well" />');
			$self.find('.friend').each(function(i){
				var res = '';
				if ($(this).hasClass('hidden')) {
				 	res += '<span class="badge badge-info" uid="'+$(this).attr('id')+'">'+$(this).find('span').html()+'</span>';
				 	$(this).hide();
				} else{
					$(this).addClass('visible');
				}
				
				$self.find('.result-box').append(res);
				$self.find('.result-box span.badge-info').live('click',function(){
					var uid = $(this).attr('uid');
					$('.friend[id="'+uid+'"]').removeClass('hidden').addClass('visible').fadeIn();					 
					$(this).remove();
					if($('.result-box span').length == 0) $('.result-box').hide();					 
				});
				 
			});
			$self.find('.friends-names .friend').live('click',function(){				 
				if($('.result-box span').length == 0) $('.result-box').show();
				$self.find('.result-box').append('<span class="badge badge-info" uid="'+$(this).attr('id')+'">'+$(this).find('span').html()+'</span>');
				$(this).removeClass('visible').addClass('hidden').fadeOut();				  
			});
			$self.prepend('<div class="input-box well form-search " />');
			$self.find('.input-box').append('<input type="text" class="input-xlarge search-query"/>');
			$self.find('.search-query').on('keyup',function(e){
				var code = (e.keyCode ? e.keyCode : e.which);
				var query = $(this).val();
				$('.friends-names .friend.visible').each(function(){	
					var itemVal = $(this).find('span').html();
					if(itemVal.indexOf(query) != -1){
						$(this).addClass('filtred').show();
					} else {
						$(this).removeClass('filtred').hide();
					}
					$('.friends-names .friend.visible.filtred.highlighted').removeClass('highlighted');
					$('.friends-names .friend.visible.filtred').first().addClass('highlighted');
					
				});
				if (code == 13 && query !== ''){					
					var matchedName = $('.friends-names .friend.visible.filtred').first();
					if($('.result-box span').length == 0) $('.result-box').show();
					$self.find('.result-box').append('<span class="badge badge-info" uid="'+matchedName.attr('id')+'">'+matchedName.find('span').html()+'</span>');
					matchedName.removeClass('visible').addClass('hidden').removeClass('filtred').removeClass('highlighted').fadeOut();
					$(this).val('');
					$(this).removeClass('filtred highlighted').show();
				}; 
			});
			$self.find('.friends-names').on('mousemove',function(){
				$('.friends-names .friend.visible.filtred.highlighted').removeClass('highlighted');
			});
		};
		
		$('.dates').on('keydown',function(){
			return false;
		});
		
		$('#friends-picker').nameAutocomplete();
		$('#startDate').datepicker();
		$('#endDate').datepicker();
		
		
	});	
}(jQuery);