/*
 *  Hover Card - v0.2.2
 *  Made by Sahil Prajapati
 */
(function( $ ) {
 
    $.fn.hoverCards = function(options) {
 
        var settings = $.extend({}, $.fn.hoverCards.defaults, options );
        var card;
        var showCard = false;
        var hCard = $('<div/>');
        var request;
        this.addClass('hover-activated');

    	$('.hover-activated').stop(true, true).hover(function(){
    		card = $(this);
    		timeout = setTimeout(function(){
            showCard = true;
            if(showCard === true){
		      	var dev_id = card.attr('data-dev-id');
		    	if(card.find('.hoverParent').length == 0){
		    		if (request != undefined){
		    			request.abort();
		    		}
			 		getData(settings.url, dev_id);
			 	}
			 	else{
			 		hCard = card.find('.hoverParent');
			 		var page_height = $(window).scrollTop();
		    		var elem_height = card.offset().top;
			 		positionCard(page_height, elem_height);	
		 		}
		 	}
		 },settings.delay);
	 	},
	    function(){
	    	//else don't show and clearout timer
            clearTimeout(timeout);
            showCard = false;
	    	card.find('.hoverParent').fadeOut(settings.fadeOut).find('.hoverCard').hide();
	    });


	    function getData(url, id){
			request = $.ajax({
		        url: "/user-data/" + id,
		        method: 'get',
		        dataType: 'json',
		        beforeSend: function(data){
		        	hCard.addClass('hoverParent').css('left','-7px').fadeIn(settings.fadeIn);//.append('<div class="hoverCard in-block">Loading..</div>');
		        	card.css('position','relative').append(hCard);
		        },
		        success: function(data){
		        	var user = data;
		          	//calling hover plugin
		          	createCard(user);
		        },
		        error:function(){
		        	createCard(user);
		        }
		      });
	    	
	    }

	    function createCard(user){
	        var data = '<div class="hoverCard"><div class="arrow-up"></div><div class="userPic" style="background-color:'+settings.backgroundColor+'"><div class="hover-img" style="background-image:url('+user.pic+')"></div>';
	        data += '<div class="userDetail"><span class="name"><strong>'+user.name+'</strong></span>';
	        data += '<p class="small role text-muted"><strong> ('+user.username+') </strong>- '+user.role+'</p>';
    		data += '<p class="about small"><strong>Online for</strong> '+calculateSince(user.online_since)+'</p>';
    		data += '<p class="small role text-muted"><strong> Level (Piscine C) : </strong>'+user.piscine_level+'</p>';
    		data += '<p class="small role text-muted"><strong> Level (42) : </strong>'+user.program_level+'</p></div></div>';
        	data += '<div class="userStats"><div><strong>Current Project(s)</strong><p>'+user.projects_inprogress.substring(0,140)+'</p></div>';
        	data += '<div><strong>Completed Project(s)</strong><p>'+user.projects_finished+'</p></div></div>';
        	attachCard(data);	        
	    }

	    function calculateSince(datetime)
		{
		    var tTime=new Date(datetime);
		    tTime.setHours(tTime.getHours() + 7);
		    var cTime=new Date();
		    var sinceMin=Math.round((cTime-tTime)/60000);
		    if(sinceMin==0)
		    {
		        var sinceSec=Math.round((cTime-tTime)/1000);
		        if(sinceSec<10)
		          var since='less than 10 seconds';
		        else if(sinceSec<20)
		          var since='less than 20 seconds';
		        else
		          var since='half a minute';
		    }
		    else if(sinceMin==1)
		    {
		        var sinceSec=Math.round((cTime-tTime)/1000);
		        if(sinceSec==30)
		          var since='half a minute';
		        else if(sinceSec<60)
		          var since='less than a minute';
		        else
		          var since='1 minute';
		    }
		    else if(sinceMin<45)
		        var since='about '+sinceMin+' minutes';
		    else if(sinceMin>44&&sinceMin<60)
		        var since='about an hour';
		    else if(sinceMin<1440){
		        var sinceHr=Math.round(sinceMin/60);
		    if(sinceHr==1)
		      var since='about an hour';
		    else
		      var since='about '+sinceHr+' hours';
		    }
		    else if(sinceMin>1439&&sinceMin<2880)
		        var since='about a day';
		    else
		    {
		        var sinceDay=Math.round(sinceMin/1440);
		        var since=sinceDay+' days';
		    }
		    return since;
		};
	        




	    function attachCard(data){
	    	var page_height = $(window).scrollTop();
	    	var elem_height = card.offset().top;
	    	hCard.html(data);
	    	positionCard(page_height, elem_height);
	    	
	    }

	    function positionCard(page_height, elem_height){
	    	var left = card.offset().left;
	    	var page_width = $(window).width();
	    	if(elem_height-page_height > 250){
	    		//top-left
	    		if(page_width - left < 335){
		    		hCard.css({'top':'-20px','height': '40px','display':'block','left':'-209px'}).find('.hoverCard').css({'bottom':'30px','top':'none','display':'block'});
		    		hCard.find('.arrow-down').show().css('left','240px');
		    		hCard.find('.arrow-up').hide().css('left','none');
	    		}//top-right
	    		else{
	    			hCard.css({'top':'-20px','height': '40px','display':'block','left':'none'}).find('.hoverCard').css({'bottom':'30px','top':'none','display':'block'});
		    		hCard.find('.arrow-down').show().css('left','32px');
		    		hCard.find('.arrow-up').hide().css('left','32px');
	    		}
	    	}
	    	else{
	    		if(page_width - left < 335){//bottom-left
		    		hCard.css({'top':'3px','height': '120px','display':'block','left':'-209px'}).find('.hoverCard').css({'top':'24px','bottom':'none','display':'block'});
		    		hCard.find('.arrow-up').show().css('left','240px');
		    		hCard.find('.arrow-down').hide().css('left','240px');
	    		}
	    		else{//bottom-right
	    			hCard.css({'top':'3px','height': '120px','display':'block','left':'none'}).find('.hoverCard').css({'top':'24px','bottom':'none','display':'block'});
		    		hCard.find('.arrow-up').show().css('left','32px');
		    		hCard.find('.arrow-down').hide().css('left','32px');
	    		}
	    	}
	    }
        return this;
 
    };
 
	$.fn.hoverCards.defaults = {
		"url":null,
		"fadeIn": 400,
		"fadeOut":200,
		"backgroundColor":'#fff',
		"delay": 300
	};

}( jQuery ));
