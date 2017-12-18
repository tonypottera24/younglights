$(function() {
    var newsArtList = {};
    newsArtList.init = function () {
        this.commonInit();
        this.bindEvent();
    };

    newsArtList.commonInit = function () {
        this.updataArtList();
    }

    newsArtList.updataArtList = function () {
        $('.newWqdArticleList').length && $('.newWqdArticleList').each(function() {
            //记录一个原始的差值
            var difHeight = $(this).parents(".sectionV2").height() - $(this).outerHeight(),
                self = this;

                $(this).data("difHeight",difHeight);

                /* 当前文章列表高度 */
                $(this).attr("eleheight",$(this).height());
                
                
                // 判断是否是默认数据
                if($(this).attr('isdemo') && $(this).attr('isdemo') == "true") {
                    return;
                }
            var $that = $(this),
                addPageDfd = $.Deferred(),
                artNavType = $that.attr('artNavType') && $that.attr('artNavType') || "CATEGORY",
                NavIds = $that.attr('navids') && $that.attr('navids') || "",
                USERID = $that.attr("userid") || "";
            /* 获取用户分类数据 */
			newsArtList.requestDate(SAAS_NEWS+"/api/news/navigationbars/"+USERID+"/"+ artNavType +"",{}, function (data) {
                newsArtList.categoryInit($that, newsArtList.getNavData(data, NavIds));
                if($that.hasClass('list1')){
                    newsArtList.loadNewsList1($that, false);
                } else if ($that.hasClass('list2')) {
                    newsArtList.loadNewsList2($that, false);
                } else if ($that.hasClass('list3')) {
                    newsArtList.loadNewsList3($that, false);
                }
                addPageDfd.resolve();
            })
            $.when(addPageDfd).done(function () {
				var touchObj = new wqdTouchSlide($that.find(".nav"),{
					bindClick : false,
					moveCallback : function(){
						
					}
				});
				/* $that.data("touchSlide",touchObj); */
			});
            
        })
    };
    // 数据请求
    newsArtList.requestDate = function (url, data, callback) {
        $.ajax({
            url:url,
			dataType:'jsonp',
			jsonp:'callback',
			type:'GET',
			data: data,
			success:callback
        });
    };
    // 加载分类导航
    newsArtList.categoryInit = function (obj,data) {
        var html= '';
        // 获取当前被选中的导航节点sourceid
        var curSourceId = obj.find('.nav span[data-sourceid].on').length && obj.find('.nav span[data-sourceid].on').attr('data-sourceid') || "";
        if(data && data.length){
            var html = "";
            if(data && data.length){
                html += '<div class="nav">'
                $.each(data, function (i, val) {
                    html +='<span data-sourceid="'+ val.id +'" class="wqd-brc wqd-bgclr"><a class="wqd-clr wqd-fw wqd-fst wqd-ff wqd-fs">'+ val.name +'</a></span>';
                })
                html += '</div>'
            }
    
            obj.find('.title-box').html(html);
            if(obj.find('.nav span').length) {
                if(curSourceId){
                    obj.find('.nav span[data-sourceid='+ curSourceId +']').length && obj.find('.nav span[data-sourceid='+ curSourceId +']').addClass('on') || obj.find('.nav span').eq(0).addClass('on');
                } else {
                    obj.find('.nav span').eq(0).addClass('on');
                }
            } else {
                // 没有导航数据
                obj.find('.title-box').html([
                    '<div class="nav">',
                        '<span class="wqd-brc wqd-bgclr"><a class="wqd-clr wqd-fw wqd-fst wqd-ff wqd-fs">没有数据</a></span>',
                    '</div>',
                ].join(''))
            };
            var allWidth = 0;
            obj.find('.title-box span').each(function () {
                allWidth += $(this).outerWidth();
            });
            // 加margin值
            allWidth += obj.find('.nav span') && (obj.find('.nav span').length)*2 || 0;
            obj.find(".nav").width(allWidth);
        } else {
            // 没有导航数据
            obj.find('.title-box').html([
                '<div class="nav">',
                    '<span class="wqd-brc wqd-bgclr"><a class="wqd-clr wqd-fw wqd-fst wqd-ff wqd-fs">没有数据</a></span>',
                '</div>',
            ].join(''))
        };
    };
    /**
     * 加载文章列表数据
     * $that 当前模块节点
     * isAdd 是否是append数据
     */
    newsArtList.loadNewsList1 = function ($that,isAdd) {
        var self = this, html = '',pageid = $that.attr('data-pageid');
        // 判断是否存在导航数据
        if($that.find('.nav span').length){
            newsArtList.requestDate(SAAS_NEWS+"/api/news/page",{
                sourceId:$that.find('.nav span.on').data('sourceid'),
                pageNo:$that.attr('pageNo') && $that.attr('pageNo') || 1,
                sortType:$that.attr('sorttype') && $that.attr('sorttype') || 'ISSUE_DATE_DESC',
                pageSize:$that.attr('row') && $that.attr('row') || 1,
                type:$that.attr('artNavType') && $that.attr('artNavType') || "CATEGORY"
            }, function (data) {
                if(data.data && data.data.length) {
                    $.each(data.data, function (i, val) {
                        var tagsHtml = '';
                        // 新闻标签
                        if(val.tags && val.tags.length){
                            $.each(val.tags, function (i, tagval) {
                                tagsHtml += '<div class="tag wqd-clr wqd-bgclr wqd-ff wqd-fw wqd-fst">'+ tagval.name +'</div>'
                            });
                        }
                        // 新闻列表
                        if(val.news){
                            html += [
                                '<a href="page_'+ pageid +'_'+ val.news.id +'.html">',
                                    '<div class="art-item clearfix">',
                                        '<div class="text-box wqd-clr wqd-ff wqd-fs wqd-fw wqd-fst">',
                                            (val.news.isRecommend == "YES" ? '<em class="recommend">推荐</em>' : ''),
                                            val.news.title,
                                        '</div>',
                                        '<div class="tag-box">',
                                            tagsHtml,
                                        '</div>',
                                        '<div class="info-box clearfix">',
                                            '<div class="info-item show-time issue-date wqd-clr wqd-bgclr wqd-fw wqd-fst">'+ val.news.issueDate +'</div>',
                                            '<div class="info-item views wqd-clr wqd-bgclr wqd-fw wqd-fst"><i>',
                                                    '<svg viewBox="0 0 48 48">',
                                                        '<path class="wqd-bgclr" d="M23.4,15.9c-4.2,0-7.7,3.6-7.7,8s3.5,8,7.7,8c1.2,0,2.3-0.3,3.3-0.8c0.5-0.2,0.7-0.9,0.5-1.4c-0.2-0.5-0.8-0.7-1.3-0.5    c-0.8,0.4-1.6,0.6-2.5,0.6c-3.1,0-5.7-2.7-5.7-5.9s2.6-5.9,5.7-5.9c3.1,0,5.7,2.7,5.7,5.9c0,0.6-0.1,1.1-0.2,1.6    c-0.1,0.6,0.1,1.1,0.7,1.3c0.5,0.2,1.1-0.2,1.2-0.7c0.2-0.7,0.3-1.5,0.3-2.2C31.1,19.5,27.7,15.9,23.4,15.9z M19.8,22.4    c-0.2,0.5-0.3,1-0.3,1.5c0,0.3,0.2,0.5,0.5,0.5c0.3,0,0.5-0.2,0.5-0.5c0-0.4,0.1-0.7,0.2-1.1c0.4-1.2,1.5-1.9,2.7-1.9    c0.3,0,0.5-0.2,0.5-0.5c0-0.3-0.2-0.5-0.5-0.5C21.8,19.8,20.4,20.9,19.8,22.4z M46.2,22.6C40.5,15.2,32.1,9.7,23.4,9.7    c-8.7,0-15.9,5.4-21.6,12.8c-0.1,0.2-0.2,0.4-0.2,0.6v1.3c0,0.2,0.1,0.5,0.2,0.6C7.5,32.6,14.7,38,23.4,38c8.7,0,17-5.4,22.8-12.9    c0.1-0.2,0.2-0.4,0.2-0.6v-1.3C46.4,23,46.4,22.8,46.2,22.6z M44.4,24.2c-5.4,6.8-13,11.8-21,11.8s-14.5-5-19.8-11.8v-0.6    C9,16.8,15.4,11.8,23.4,11.8c8,0,15.6,5,21,11.8C44.4,23.6,44.4,24.2,44.4,24.2z"></path>',
                                                    '</svg>',
                                            '</i>'+ newsArtList.setFormat("listView",(val.news.initialPageView+val.news.pageView)) +'</div>',
                                            '<div class="info-item goods wqd-clr wqd-bgclr wqd-fw wqd-fst">',
                                            '<i>',
                                                '<svg viewBox="0 0 48 48">',
                                                    '<path class="st0 wqd-bgclr" d="M36.4,19.2C36,19,35.5,19,34.9,19H31c0.5-2.3,0.6-5.6,0.6-7.6c0-2.3-1.9-4.2-4.2-4.2c-2.3,0-4.2,1.9-4.2,4.2    v0.8c0,4.6-3.7,8.3-8.2,8.4c-0.1,0-0.1,0-0.2,0h-4.2c-1.9,0-3.4,1.5-3.4,3.4v13.4c0,1.9,1.5,3.4,3.4,3.4h4.2    c0.4,0,0.8-0.4,0.8-0.9V22.2c5.2-0.4,9.3-4.7,9.3-10v-0.8c0-1.3,1.1-2.5,2.5-2.5c1.3,0,2.5,1.1,2.5,2.5c0,3.8-0.3,6.8-0.8,8.1    c-0.1,0.2,0,0.5,0.1,0.8c0.1,0.2,0.4,0.4,0.7,0.4h5c0.4,0,0.8,0,1.1,0.1c2.3,0.6,3.6,2.9,3,5.1c-0.7,2.5-4.1,11.2-4.4,12    c-0.5,0.8-1.2,1.2-2.2,1.2H19.8c-0.4,0-0.8,0.3-0.8,0.8c0,0.4,0.3,0.8,0.8,0.8h12.6c0,0,0.1,0,0.2,0c1.4,0,2.7-0.8,3.5-2.1    c0,0,0,0,0-0.1c0.1-0.4,3.8-9.6,4.5-12.2C41.4,23.3,39.6,20,36.4,19.2z M13.9,39h-3.4c-0.9,0-1.7-0.8-1.7-1.7V23.9    c0-0.9,0.8-1.7,1.7-1.7h3.4V39z"></path>',
                                                '</svg>',
                                            '</i>'+ newsArtList.setFormat("listAmount",(val.news.initialPraiseAmount+val.news.praiseAmount)) +'</div>',
                                        '</div>',
                                        '<div class="line-box clearfix">',
                                            '<hr class="bottom-line wqd-brc wqd-brw">',
                                        '</div>',
                                    '</div>',
                                '</a>'
                            ].join('');
                        }
                    });
                    if(isAdd){
                        // append数据
                        $that.find('.content-box').length && $that.find('.content-box').append(html);
                    } else {
                        $that.find('.content-box').length && $that.find('.content-box').html(html);
                    }
                   
                } else {
                    html += '<div style="text-align:center;padding-top:20px;" class="no-msg">没有数据了</div>';
                    $that.find('.content-box').length && $that.find('.content-box').html(html);
                }
                newsArtList.setListConf($that, {
                    pageNo:data.pageNo,
                    totalPages:data.totalPages,
                    totalCount:data.totalCount
                });
                
                /* 添加属性值 */
                // $that.attr({
                //     pageno:data.pageNo,
                //     totalpages:data.totalPages,
                // });
                // // 判断加载更多
                // if(!(data.pageNo > data.totalPages)){
                //     $that.find('.load-more.no-load').length && $that.find('.load-more').removeClass('no-load');
                // }

                // // if(data.pageNo == data.totalPages || data.pageNo > data.totalPages){
                // //     if(!$that.find('.no-msg').length){
                // //         $that.find('.content-box').append('<div style="text-align:center;padding-top:20px;" class="no-msg">没有数据了</div>');
                // //     }
                // //     $that.find('.load-more').length && $that.find('.load-more').addClass('no-load');
                // // } else {
                // //     $that.find('.load-more').length && $that.find('.load-more').show();
                // //     !$that.find('.load-more').length && $that.find('.artList-container').append('<div class="load-more small wqd-fw wqd-fst wqd-ff wqd-bgclr wqd-clr">加载更多</div>')
                // // }

                //  //重新计算通栏的高度
                // // var difHeight1 =  $that.data("difHeight") || 0;
                // // data.data && data.data.length && $that.parents(".sectionV2").height($that.outerHeight()+difHeight1);


                // //  //重新定位后面的元素
                // var $elems =  $that.parents('.sectionV2').find('.wqdelementEdit');
                // $elems.each(function(_i, _val){
                //     // 判断是否为该元素下面的元素
                //     if($that[0].offsetTop < _val.offsetTop){
                //         $(_val).css('top',_val.offsetTop+($that.outerHeight() - $that.attr('eleheight')));
                //     }
                // })
                //  //重置通栏高度
                // var eleHeight =  $that.attr("eleheight");
                //     $that.parents(".sectionV2").height($that.parents(".sectionV2").outerHeight()+ ($that.outerHeight() - eleHeight));
                //     $that.attr("eleheight", $that.outerHeight());
            })
        } else {
            // 不存在导航数据
            // $that.find('.content-box').html('<div style="font-size:16px;font-weight:600;text-align:center;padding-top:20px;">没有数据</div>')

        }
    };
    newsArtList.loadNewsList2 = function ($that,isAdd) {
		var self = this, html = '',pageid = $that.attr('data-pageid');
        /* 获取文章列表2 */
        if($that.find('.nav span').length){
            newsArtList.requestDate(SAAS_NEWS+"/api/news/page",{
                sourceId:$that.find('.nav span.on').data('sourceid'),
                pageNo:$that.attr('pageNo') && $that.attr('pageNo') || 1,
                sortType:$that.attr('sorttype') && $that.attr('sorttype') || 'ISSUE_DATE_DESC',
                pageSize:$that.attr('row') && $that.attr('row') || 1,
                type:$that.attr('artNavType') && $that.attr('artNavType') || "CATEGORY"
            }, function (data) {
                if(data.data && data.data.length) {
                    $.each(data.data, function (i, val) {
                        var tagsHtml = '',imgHtml="";
                        // 新闻标签
                        if(val.tags && val.tags.length){
                            $.each(val.tags, function (i, tagval) {
                                tagsHtml += '<div class="tag wqd-clr wqd-bgclr wqd-ff wqd-fw wqd-fst">'+ tagval.name +'</div>'
                            });
                        }
                        // 新闻图片
                        if(val.news && val.news.coverPicture) {
                            // 有图
                            imgHtml +=['<div class="img-box">',
                                            '<img src="'+(!!val.news.coverPicture.split(',')[0] ? (/(http)|(https)/gi.test(val.news.coverPicture.split(',')[0])?(val.news.coverPicture.split(',')[0]):(CSSURLPATH + val.news.coverPicture.split(',')[0])) : '/images/news-demo/wqd_no_img.png')+'" onerror="onerror = null;this.src=\'/images/news-demo/imgerror.png\';" alt="">',
                                            '<img src="'+(!!val.news.coverPicture.split(',')[1] ? (/(http)|(https)/gi.test(val.news.coverPicture.split(',')[1])?(val.news.coverPicture.split(',')[1]):(CSSURLPATH + val.news.coverPicture.split(',')[1])) : '/images/news-demo/wqd_no_img.png')+'" onerror="onerror = null;this.src=\'/images/news-demo/imgerror.png\';" alt="">',
                                            '<img src="'+(!!val.news.coverPicture.split(',')[2] ? (/(http)|(https)/gi.test(val.news.coverPicture.split(',')[2])?(val.news.coverPicture.split(',')[2]):(CSSURLPATH + val.news.coverPicture.split(',')[2])) : '/images/news-demo/wqd_no_img.png')+'" onerror="onerror = null;this.src=\'/images/news-demo/imgerror.png\';" alt="">',
                                        '</div>'].join('');
                        } else {
                            // 没图
                            imgHtml +=['<div class="img-box">',
                                        '<img src="/images/news-demo/wqd_no_img.png" alt="">',
                                        '<img src="/images/news-demo/wqd_no_img.png" alt="">',
                                        '<img src="/images/news-demo/wqd_no_img.png" alt="">',
                                    '</div>'].join('');
                        }
                        // 新闻列表
                        if(val.news){
                            html += [
                                '<a href="page_'+ pageid +'_'+ val.news.id +'.html">',
                                    '<div class="art-item clearfix">',
                                        '<div class="text-box wqd-clr wqd-ff wqd-fs wqd-fw wqd-fst">',
                                            (val.news.isRecommend == "YES" ? '<em class="recommend">推荐</em>' : ''),
                                            val.news.title,
                                        '</div>',
                                            imgHtml,
                                        '<div class="tag-box">',
                                            tagsHtml,
                                        '</div>',
                                        '<div class="info-box clearfix">',
                                            '<div class="info-item show-time issue-date wqd-clr wqd-bgclr wqd-fw wqd-fst">'+ val.news.issueDate +'</div>',
                                            '<div class="info-item views wqd-clr wqd-bgclr wqd-fw wqd-fst"><i>',
                                                    '<svg viewBox="0 0 48 48">',
                                                        '<path class="wqd-bgclr" d="M23.4,15.9c-4.2,0-7.7,3.6-7.7,8s3.5,8,7.7,8c1.2,0,2.3-0.3,3.3-0.8c0.5-0.2,0.7-0.9,0.5-1.4c-0.2-0.5-0.8-0.7-1.3-0.5    c-0.8,0.4-1.6,0.6-2.5,0.6c-3.1,0-5.7-2.7-5.7-5.9s2.6-5.9,5.7-5.9c3.1,0,5.7,2.7,5.7,5.9c0,0.6-0.1,1.1-0.2,1.6    c-0.1,0.6,0.1,1.1,0.7,1.3c0.5,0.2,1.1-0.2,1.2-0.7c0.2-0.7,0.3-1.5,0.3-2.2C31.1,19.5,27.7,15.9,23.4,15.9z M19.8,22.4    c-0.2,0.5-0.3,1-0.3,1.5c0,0.3,0.2,0.5,0.5,0.5c0.3,0,0.5-0.2,0.5-0.5c0-0.4,0.1-0.7,0.2-1.1c0.4-1.2,1.5-1.9,2.7-1.9    c0.3,0,0.5-0.2,0.5-0.5c0-0.3-0.2-0.5-0.5-0.5C21.8,19.8,20.4,20.9,19.8,22.4z M46.2,22.6C40.5,15.2,32.1,9.7,23.4,9.7    c-8.7,0-15.9,5.4-21.6,12.8c-0.1,0.2-0.2,0.4-0.2,0.6v1.3c0,0.2,0.1,0.5,0.2,0.6C7.5,32.6,14.7,38,23.4,38c8.7,0,17-5.4,22.8-12.9    c0.1-0.2,0.2-0.4,0.2-0.6v-1.3C46.4,23,46.4,22.8,46.2,22.6z M44.4,24.2c-5.4,6.8-13,11.8-21,11.8s-14.5-5-19.8-11.8v-0.6    C9,16.8,15.4,11.8,23.4,11.8c8,0,15.6,5,21,11.8C44.4,23.6,44.4,24.2,44.4,24.2z"></path>',
                                                    '</svg>',
                                            '</i>'+ newsArtList.setFormat("listView",(val.news.initialPageView+val.news.pageView)) +'</div>',
                                            '<div class="info-item goods wqd-clr wqd-bgclr wqd-fw wqd-fst">',
                                            '<i>',
                                                '<svg viewBox="0 0 48 48">',
                                                    '<path class="st0 wqd-bgclr" d="M36.4,19.2C36,19,35.5,19,34.9,19H31c0.5-2.3,0.6-5.6,0.6-7.6c0-2.3-1.9-4.2-4.2-4.2c-2.3,0-4.2,1.9-4.2,4.2    v0.8c0,4.6-3.7,8.3-8.2,8.4c-0.1,0-0.1,0-0.2,0h-4.2c-1.9,0-3.4,1.5-3.4,3.4v13.4c0,1.9,1.5,3.4,3.4,3.4h4.2    c0.4,0,0.8-0.4,0.8-0.9V22.2c5.2-0.4,9.3-4.7,9.3-10v-0.8c0-1.3,1.1-2.5,2.5-2.5c1.3,0,2.5,1.1,2.5,2.5c0,3.8-0.3,6.8-0.8,8.1    c-0.1,0.2,0,0.5,0.1,0.8c0.1,0.2,0.4,0.4,0.7,0.4h5c0.4,0,0.8,0,1.1,0.1c2.3,0.6,3.6,2.9,3,5.1c-0.7,2.5-4.1,11.2-4.4,12    c-0.5,0.8-1.2,1.2-2.2,1.2H19.8c-0.4,0-0.8,0.3-0.8,0.8c0,0.4,0.3,0.8,0.8,0.8h12.6c0,0,0.1,0,0.2,0c1.4,0,2.7-0.8,3.5-2.1    c0,0,0,0,0-0.1c0.1-0.4,3.8-9.6,4.5-12.2C41.4,23.3,39.6,20,36.4,19.2z M13.9,39h-3.4c-0.9,0-1.7-0.8-1.7-1.7V23.9    c0-0.9,0.8-1.7,1.7-1.7h3.4V39z"></path>',
                                                '</svg>',
                                            '</i>'+ newsArtList.setFormat("listAmount",(val.news.initialPraiseAmount+val.news.praiseAmount)) +'</div>',
                                        '</div>',
                                        '<div class="line-box clearfix">',
                                            '<hr class="bottom-line wqd-brc wqd-brw">',
                                        '</div>',
                                    '</div>',
                                '</a>'
                            ].join('');
                        }
                    });
                    if(isAdd){
                        // append数据
                        $that.find('.content-box').length && $that.find('.content-box').append(html);
                    } else {
                        $that.find('.content-box').length && $that.find('.content-box').html(html);
                    }
                } else {
                    html += '<div style="text-align:center;padding-top:20px;" class="no-msg">没有数据了</div>';
                    $that.find('.content-box').length && $that.find('.content-box').html(html);
                }
                
                newsArtList.setListConf($that, {
                    pageNo:data.pageNo,
                    totalPages:data.totalPages,
                    totalCount:data.totalCount
                });
                /* 添加属性值 */
                // $that.attr({
                //     pageno:data.pageNo,
                //     totalpages:data.totalPages,
                // });
                // // 判断是否有加载更多
                // if(!(data.pageNo > data.totalPages)){
                //     $that.find('.load-more.no-load').length && $that.find('.load-more').removeClass('no-load');
                // }

                // // if(data.pageNo == data.totalPages || data.pageNo > data.totalPages){
                // //     $that.find('.load-more').length && $that.find('.load-more').remove();
                // // } else {
                // //     $that.find('.load-more').length && $that.find('.load-more').show();
                // //     !$that.find('.load-more').length && $that.find('.artList-container').append('<div class="load-more small wqd-fw wqd-fst wqd-ff wqd-bgclr wqd-clr">加载更多</div>')
                // // }
                // //重新计算通栏的高度
                // // var difHeight =  $that.data("difHeight") || 0;
                // // data.data && data.data.length && $that.parents(".sectionV2").height($that.outerHeight()+difHeight);
                // //  //重新定位后面的元素
                // var $elems =  $that.parents('.sectionV2').find('.wqdelementEdit');
                // $elems.each(function(_i, _val){
                //     // 判断是否为该元素下面的元素
                //     if($that[0].offsetTop < _val.offsetTop){
                //         $(_val).css('top',_val.offsetTop+($that.outerHeight() - $that.attr('eleheight')));
                //     }
                // })
                //  //重置通栏高度
                // var eleHeight =  $that.attr("eleheight");
                //     $that.parents(".sectionV2").height($that.parents(".sectionV2").outerHeight()+ ($that.outerHeight() - eleHeight));
                //     $that.attr("eleheight", $that.outerHeight());
            });
        }else {
            // 不存在导航数据
            // $that.find('.content-box').html('<div style="font-size:16px;font-weight:600;text-align:center;padding-top:20px;">没有数据</div>')
        }
    };
    newsArtList.loadNewsList3 = function ($that,isAdd) {
		var self = this, html = '',pageid = $that.attr('data-pageid');
        /* 获取文章列表3 */
        if($that.find('.nav span').length){
            newsArtList.requestDate(SAAS_NEWS+"/api/news/page",{
                sourceId:$that.find('.nav span.on').data('sourceid'),
                pageNo:$that.attr('pageNo') && $that.attr('pageNo') || 1,
                sortType:$that.attr('sorttype') && $that.attr('sorttype') || 'ISSUE_DATE_DESC',
                pageSize:$that.attr('row') && $that.attr('row') || 1,
                type:$that.attr('artNavType') && $that.attr('artNavType') || "CATEGORY"
            }, function (data) {
                if(data.data && data.data.length) {
                    $.each(data.data, function (i, val) {
                        var imgHtml = "";
                        if(val.news.coverPicture && val.news.coverPicture.split(",").length) {
                            imgHtml = '<img src="'+ (!!val.news.coverPicture.split(',')[0] ? (/(http)|(https)/gi.test(val.news.coverPicture.split(',')[0])?(val.news.coverPicture.split(',')[0]):(CSSURLPATH + val.news.coverPicture.split(',')[0])) : '/images/news-demo/wqd_no_img.png') +'" onerror="onerror = null;this.src=\'/images/news-demo/imgerror.png\';" alt="">'
                        } else {
                            imgHtml = '<img src="/images/news-demo/wqd_no_img.png" alt="">'
                        }
                        // 新闻列表
                        if(val.news){
                            html += [
                                '<a href="page_'+ pageid +'_'+ val.news.id +'.html">',
                                    '<div class="art-item clearfix">',
                                        '<div class="img-box">',
                                            imgHtml,
                                        '</div>',
                                        '<div class="art-info">',
                                            '<div class="text-box wqd-clr wqd-ff wqd-fs wqd-fw wqd-fst">',
                                                (val.news.isRecommend == "YES" ? '<em class="recommend">推荐</em>' : ''),
                                                val.news.title,
                                            '</div>',
                                            '<div class="describe wqd-clr wqd-bgclr wqd-ff wqd-fw wqd-fst">'+ val.news.digest +'</div>',
                                            '<div class="info-box clearfix">',
                                                '<div class="tag-box">',
                                                    '<div style="display:none" class="tag wqd-clr wqd-bgclr wqd-ff wqd-fw wqd-fst">默认标签</div>',
                                                '</div>',
                                                '<div class="info-item show-time issue-date wqd-clr wqd-bgclr wqd-fw wqd-fst">'+ val.news.issueDate +'</div>',
                                                '<div class="info-item views wqd-clr wqd-bgclr wqd-fw wqd-fst"><i>',
                                                    '<svg viewBox="0 0 48 48">',
                                                        '<path class="wqd-bgclr" d="M23.4,15.9c-4.2,0-7.7,3.6-7.7,8s3.5,8,7.7,8c1.2,0,2.3-0.3,3.3-0.8c0.5-0.2,0.7-0.9,0.5-1.4c-0.2-0.5-0.8-0.7-1.3-0.5    c-0.8,0.4-1.6,0.6-2.5,0.6c-3.1,0-5.7-2.7-5.7-5.9s2.6-5.9,5.7-5.9c3.1,0,5.7,2.7,5.7,5.9c0,0.6-0.1,1.1-0.2,1.6    c-0.1,0.6,0.1,1.1,0.7,1.3c0.5,0.2,1.1-0.2,1.2-0.7c0.2-0.7,0.3-1.5,0.3-2.2C31.1,19.5,27.7,15.9,23.4,15.9z M19.8,22.4    c-0.2,0.5-0.3,1-0.3,1.5c0,0.3,0.2,0.5,0.5,0.5c0.3,0,0.5-0.2,0.5-0.5c0-0.4,0.1-0.7,0.2-1.1c0.4-1.2,1.5-1.9,2.7-1.9    c0.3,0,0.5-0.2,0.5-0.5c0-0.3-0.2-0.5-0.5-0.5C21.8,19.8,20.4,20.9,19.8,22.4z M46.2,22.6C40.5,15.2,32.1,9.7,23.4,9.7    c-8.7,0-15.9,5.4-21.6,12.8c-0.1,0.2-0.2,0.4-0.2,0.6v1.3c0,0.2,0.1,0.5,0.2,0.6C7.5,32.6,14.7,38,23.4,38c8.7,0,17-5.4,22.8-12.9    c0.1-0.2,0.2-0.4,0.2-0.6v-1.3C46.4,23,46.4,22.8,46.2,22.6z M44.4,24.2c-5.4,6.8-13,11.8-21,11.8s-14.5-5-19.8-11.8v-0.6    C9,16.8,15.4,11.8,23.4,11.8c8,0,15.6,5,21,11.8C44.4,23.6,44.4,24.2,44.4,24.2z"></path>',
                                                    '</svg>',
                                                '</i>'+ newsArtList.setFormat("listView",(val.news.initialPageView+val.news.pageView)) +'</div>',
                                                '<div class="info-item goods wqd-clr wqd-bgclr wqd-fw wqd-fst"><i>',
                                                    '<svg viewBox="0 0 48 48">',
                                                        '<path class="st0 wqd-bgclr" d="M36.4,19.2C36,19,35.5,19,34.9,19H31c0.5-2.3,0.6-5.6,0.6-7.6c0-2.3-1.9-4.2-4.2-4.2c-2.3,0-4.2,1.9-4.2,4.2    v0.8c0,4.6-3.7,8.3-8.2,8.4c-0.1,0-0.1,0-0.2,0h-4.2c-1.9,0-3.4,1.5-3.4,3.4v13.4c0,1.9,1.5,3.4,3.4,3.4h4.2    c0.4,0,0.8-0.4,0.8-0.9V22.2c5.2-0.4,9.3-4.7,9.3-10v-0.8c0-1.3,1.1-2.5,2.5-2.5c1.3,0,2.5,1.1,2.5,2.5c0,3.8-0.3,6.8-0.8,8.1    c-0.1,0.2,0,0.5,0.1,0.8c0.1,0.2,0.4,0.4,0.7,0.4h5c0.4,0,0.8,0,1.1,0.1c2.3,0.6,3.6,2.9,3,5.1c-0.7,2.5-4.1,11.2-4.4,12    c-0.5,0.8-1.2,1.2-2.2,1.2H19.8c-0.4,0-0.8,0.3-0.8,0.8c0,0.4,0.3,0.8,0.8,0.8h12.6c0,0,0.1,0,0.2,0c1.4,0,2.7-0.8,3.5-2.1    c0,0,0,0,0-0.1c0.1-0.4,3.8-9.6,4.5-12.2C41.4,23.3,39.6,20,36.4,19.2z M13.9,39h-3.4c-0.9,0-1.7-0.8-1.7-1.7V23.9    c0-0.9,0.8-1.7,1.7-1.7h3.4V39z"></path>',
                                                    '</svg>',
                                                '</i>'+ newsArtList.setFormat("listAmount",(val.news.initialPraiseAmount+val.news.praiseAmount)) +'</div>',
                                            '</div>',
                                        '</div>',
                                        '<div class="line-box clearfix">',
                                            '<hr class="bottom-line wqd-brc wqd-brw">',
                                        '</div>',
                                    '</div>',
                                '</a>'
                            ].join('');
                        }
                    });
                    $that.find('.artList-container').addClass('three');
                    if(isAdd){
                        // append数据
                        $that.find('.content-box').length && $that.find('.content-box').append(html);
                        
                    } else {
                        $that.find('.content-box').length && $that.find('.content-box').html(html);
                    }
                } else {
                    html += '<div style="text-align:center;padding-top:20px;" class="no-msg">没有数据了</div>';
                    $that.find('.content-box').length && $that.find('.content-box').html(html);
                }
                
                
                newsArtList.setListConf($that, {
                    pageNo:data.pageNo,
                    totalPages:data.totalPages,
                    totalCount:data.totalCount
                });
                
            });
        } else {
            // 不存在导航数据
            // $that.find('.content-box').html('<div style="font-size:16px;font-weight:600;text-align:center;padding-top:20px;">没有数据</div>')
        }
	}
    // 绑定事件
    newsArtList.bindEvent = function () {
        $(document).on('click.cateClick','.nav span', function () {
            // 先判断是否有分类
            $(this).addClass('on').siblings('span').removeClass('on');
			if($(this).attr('data-sourceid')){
                if($(this).hasClass('on')){
                    var $that = $(this).parents('.newWqdArticleList');
                    /* 清除节点 pageno totalpages 属性*/
                    $(this).parents('.newWqdArticleList').removeAttr('isend pageno totalpages');
                    if($that.hasClass('list1')){
                        newsArtList.loadNewsList1($that,false);
                    } else if ($that.hasClass('list2')) {
                        newsArtList.loadNewsList2($that,false);
                    } else if ($that.hasClass('list3')) {
                        newsArtList.loadNewsList3($that,false);
                    }
                }
            }
        })
        // 点击加载更多
        $(document).on('click.loadmore', '.newWqdArticleList[loadtype!="scroload"] .load-more', function () {
            newsArtList.loadmore($(this));
        });
        //滑动加载
		$(window).on("scroll", function() {
            var $this = $(".newWqdArticleList[loadtype='scroload'] .load-more");
            if(!$this.length) return;

            var inview = $this.filter(function() {
                var $e = $(this), $w = $(window), wt = $w.scrollTop(), wb = wt + $w.height(), et = $e.offset().top, eb = et + $e.height();
	            return et >= wt && eb <= wb && $e.is(":visible");
            });
	        inview.each(function(i, _val){
                newsArtList.loadmore($(_val));
            });
		});
    };
    // 加载更多 $this 加载更多按钮
    newsArtList.loadmore = function ($this) {
        if($this.hasClass('no-load')) return;
        var $that = $this.parents('.newWqdArticleList'),
            pageNo = $this.parents('.newWqdArticleList').attr('pageno') && parseInt($this.parents('.newWqdArticleList').attr('pageno'))+1 || 1,
            totalCount = $this.parents('.newWqdArticleList').attr('totalcount') && parseInt($this.parents('.newWqdArticleList').attr('totalcount')),
            row = $this.parents('.newWqdArticleList').attr('row') && parseInt($this.parents('.newWqdArticleList').attr('row')) || 1;
            
        if($that.attr('isdemo')=="true") return;
        /* 加一层判断 */
        if(!((pageNo - 1)*row > $that.find('.art-item').length)){
            if(!(parseInt(pageNo) > parseInt($that.attr('totalpages')))){
                $this.parents('.newWqdArticleList').attr('pageno', pageNo);
                if($that.hasClass('list1')){
                    newsArtList.loadNewsList1($that,true);
                } else if ($that.hasClass('list2')) {
                    newsArtList.loadNewsList2($that,true);
                } else if ($that.hasClass('list3')) {
                    newsArtList.loadNewsList3($that,true);
                }
            }
        }
    };
    newsArtList.setListConf = function ($that, data) {
        /* 添加属性值 */
        $that.attr({
            pageno:data.pageNo,
            totalpages:data.totalPages,
            totalcount:data.totalCount
        })
        // 判断加载更多
        if(data.pageNo == data.totalPages){
            $that.find('.load-more').length && $that.find('.load-more').addClass('no-load');
            if(!$that.find('.no-msg').length){
                $that.find('.content-box').append('<div style="text-align:center;padding-top:20px;" class="no-msg">没有数据了</div>');
            }
            $that.find('.load-more').length && $that.find('.load-more').hide();
        } else {
            !$that.find('.load-more').length && $that.find('.artList-container').append('<div class="load-more small wqd-fw wqd-fst wqd-ff wqd-bgclr wqd-clr">加载更多</div>')
            $that.find('.load-more.no-load').length && $that.find('.load-more').removeClass('no-load');
            $that.find('.load-more').length && $that.find('.load-more').show();
        }

         //重新定位后面的元素
        var $elems =  $that.parents('.sectionV2').find('.wqdelementEdit');
        $elems.each(function(_i, _val){
            // 判断是否为该元素下面的元素
            if($that[0].offsetTop < _val.offsetTop){
                $(_val).css('top',_val.offsetTop+($that.outerHeight() - $that.attr('eleheight')));
            }
        })
         //重置通栏高度
        var eleHeight =  $that.attr("eleheight");
        $that.parents(".sectionV2").height($that.parents(".sectionV2").outerHeight()+ ($that.outerHeight() - eleHeight));
        $that.attr("eleheight", $that.outerHeight());
    }
    /**
     * 筛选导航数据
     * dataArr 获取的导航全部数据
     * NavIds 所选导航数据数组
     */
    newsArtList.getNavData = function (dataArr,NavIds) {
        var newArr = [];
    	if(NavIds){
			NavIds = NavIds.split(",");
			$.each(NavIds,function(_i,_val){
				for(var k=0; k<dataArr.length; k++){
					if(parseInt(_val)== dataArr[k].id){
                        newArr.push(dataArr[k]);
                        break;
					}
				}	
			});
			return newArr;
		}
    };

    /**
     * 格式化设置
     * type 类型
     * val 值
     */     
    newsArtList.setFormat = function (type, val) {
        if(type == "listAmount" || type == "listView"){
            if(!(val<10000)){
                return (val/10000).toFixed(1) + 'w';
            } else {
                return val
            }
        }
    }
    
    newsArtList.init();
})