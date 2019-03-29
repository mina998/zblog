$(function () {
    var E = window.wangEditor
    var editor = new E('#editor')
    var $text1 = $('.wangEditor')
    editor.customConfig.onchange = function (html) {
        // 监控变化，同步更新到 textarea
        $text1.val(html)
    }
    editor.customConfig.uploadImgServer = '/admin/image/up'
    editor.customConfig.uploadImgMaxSize = 2 * 1024 * 1024
    editor.customConfig.uploadImgMaxLength = 3

    editor.create()
    E.fullscreen.init(editor);
    E.viewSource.init(editor);
    // 初始化 textarea 的值
    editor.txt.html($text1.text())
    $text1.val(editor.txt.html())

    // Tags标签效果 //
    $('#collapse a.label').click(function () {
        tag = $(this).text()
        $(this).removeClass('label-info').addClass('label-success')
        tags = $('input#tag')
        if (tags.val() == ''){
            tags.val(tag)
        }else {
            tags.val(tags.val()+','+tag)
        }
    })
})