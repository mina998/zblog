//导航菜单
mods = eval(document.getElementById('uiMods').getAttribute('data'))
uicc = eval(document.getElementById('uiMods').getAttribute('layui'))
uicc = uicc ? uicc : function(ui){}

layui.use(mods, function (){
    $ = layui.jquery
    layer = layui.layer
    uicc(layui)
    //搜索
    $('.fly-search').on('click', function(){
        layer.open({
            type: 1
            ,title: false
            ,closeBtn: false
            ,shadeClose: true
            ,maxWidth: 10000
            ,skin: 'fly-layer-search'
            ,content: [
                '<form action="https://www.baidu.com/s">'
                ,'<input autocomplete="off" placeholder="搜索内容，回车跳转" type="text" name="wd">'
                ,'</form>'
            ].join('')
            ,success: function(layero){
                var input = layero.find('input')
                input.focus();

                layero.find('form').submit(function(){
                    var val = input.val()
                    if(val.replace(/\s/g, '') === ''){
                        return false
                    }
                    input.val('site:www.skiss.cc '+ input.val())
                })
            }
        })
    })
})


//Post页面Js代码
function post(ui) {
    form   = ui.form
    layedit = ui.layedit

    // 配置编辑器
    config ={
        height: 180,
        tool: ['left', 'center', 'right', '|', 'face']
    }
    index = layedit.build('comment',config)

    // 自定义表单验证器
    form.verify({
        nickname: function(value, item){ //value：表单的值、item：表单的DOM对象
            if(!new RegExp("^[a-zA-Z0-9_\u4e00-\u9fa5\\s·]+$").test(value)){
                return '昵称不能有特殊字符';
            }
            if (value.length > 22){
                return '昵称长度不能超过22个字符';
            }
        },
        comment: function(value, item){ //value：表单的值、item：表单的DOM对象
            value = layedit.getContent(index)
            if(value == ''){
                return '评论内容不能为空'
            }
            if (value.length > 250){
                return '评论内容长度不能超过250个字符'
            }
            return layedit.sync(index)
        }
    })

    //表单提交
    form.on('submit(*)', function(data){
        //人机验证
        if ($('input[name="vaptcha_token"]').attr('value') == undefined){
            layer.tips('请先进行人机验证', '.vp-basic-btn');
            return false
        }
        //Ajax服务端验证
        $.post($(data.form).attr('action'), data.field, function(res){
            if (typeof res == "string"){
                res = $.parseJSON(res)
            }
            //检测Email
            if (res.msg.email){
                    layer.tips(res.msg.email[0], '#email',{
                    tips: [1, '#000'],
                })
                return false
            }
            //检测昵称
            if (res.msg.name){
                    layer.tips(res.msg.name[0], '#name',{
                    tips: [1, '#000'],
                })
                return false
            }
            //检测评论内容
            if (res.msg.comment){
                    layer.tips(res.msg.comment[0], '.layui-layedit-iframe',{
                    tips: [1, '#000'],
                })
                return false
            }
            //人机验证
            if (res.msg.vaptcha_token){
                    layer.tips(res.msg.vaptcha_token[0], '.vp-basic-cont',{
                    tips: [1, '#000'],
                })
                return false
            }
            //编辑器内容同步
            if (res.action){
                window.location.reload()
                location.href = window.location.pathname+'#comment'
            }
        })
        return false;
    })

    // 编辑器插入代码
    $('.comment .fly-badge-vip').click(function () {
        us = $(this).siblings('cite').text()
        id = $(this).siblings('cite').attr('data')
        layedit.setContent(index, '<a href="#'+id+'">@'+us+'</a> &nbsp;',1)
    })

    //代码美化
    $('blockquote').addClass('layui-elem-quote')
    $('pre').each(function () {
        html = $(this).html()
        $(this).html(html.replace(/<br>/g, '\n')).addClass('prettyprint linenums')
    })
    if($('pre').length > 0) {
        window.prettyPrint()
    }
/*--*/
}

//Classify页面Js代码
function classify(ui) {
    //...
}