//后台菜单选中
href = window.location.pathname
if (href == '/admin/classify/add'){
	href = '/admin/classify'
}
if (href.indexOf('/admin/classify/edit/')===0){
	href = '/admin/classify'
}
if (href.indexOf('/admin/post/edit/')===0){
	href = '/admin/post'
}
$('section.sidebar a').each(function () {
	th = $(this).attr('href')
    if(th == window.location.pathname || th == href){
        $(this).parent('li').addClass('active')
        return false
    }
})


//选择Tag标签
$('#collapse a').click(function () {
	tags = $('input#tags').val()+','+$(this).text()
	$('input#tags').val(tags.replace(/^,/g,''))
})

// 上传图片
if ($('input#cover').length > 0){
	$('input#cover').get(0).onchange = function() {
		file = this.files[0]
		if (file.size > 1024*1024*1.5) {
			alert('图片大小不能超过1.5M')
			return false
		}
		// console.log(file);
		var reader = new FileReader()
		reader.readAsDataURL(file)
		reader.onload = function(){
			$('img.cover').attr('src', this.result)
		}
	}
}
//删除图片
$('.del.btn').click(function () {
	cover = '/static/images/upfile.png'
	field = $(this).attr('data')
	avatar= $('.card.cover')
	if (avatar.attr('src') != cover){
		$.get(window.location.pathname,{'cover':'del'},function (res) {
			console.log(res)
			if (res.err==0){
				alert('头像删除成功!')
				avatar.attr('src',cover)
				return false
			}
			alert('删除失败!')
		})
	}

})









$('.btn.post.del').click(function () {
	locations('/admin/post/del','将删除和文章相关的所有标签和评论!')
})


$('.btn.review.up').click(function () {
	locations('/admin/review/up/')
})


//
function del(msg){
	if(confirm(msg)){
		return true
	}else{
		return false
	}
}

function locations(url,msg='确认操作吗?') {
	if(confirm(msg)){
        all = ''
        $("input[name='id']:checked").each(function (i) {
            all += $(this).val() + ','
        })
        window.location.href= url+'?all='+all
		return true
	}else{
		return false
	}
}
