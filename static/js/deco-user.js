// 修改个人中心邮箱验证码 GET
function sendCodeChangeEmail($btn) {
    var verify = verifyDialogSubmit(
        [
            {id: '#jsChangeEmail', tips: Dml.Msg.epMail, errorTips: Dml.Msg.erMail, regName: 'email', require: true}
        ]
    );
    if (!verify) {
        return;
    }
    $.ajax({
        cache: false,
        type: "get",
        dataType: 'json',
        url: update_email_url,
        data: $('#jsChangeEmailForm').serialize(),
        async: true,
        beforeSend: function () {
            $btn.val("发送中...");
            $btn.attr('disabled', true);
        },
        success: function (data) {
            if (data.email) {
                Dml.fun.showValidateError($('#jsChangeEmail'), data.email);
            } else if (data.status === 'success') {
                Dml.fun.showErrorTips($('#jsChangeEmailTips'), "邮箱验证码已发送");
            } else if (data.status === 'failure') {
                Dml.fun.showValidateError($('#jsChangeEmail'), "当前邮箱已被绑定，发送失败");
            }
        },
        complete: function () {
            $btn.val("获取验证码");
            $btn.removeAttr("disabled");
        }
    });

}

// 个人资料邮箱修改 POST
function changeEmailSubmit($btn) {
    var verify = verifyDialogSubmit(
        [
            {id: '#jsChangeEmail', tips: Dml.Msg.epMail, errorTips: Dml.Msg.erMail, regName: 'email', require: true},
        ]
    );
    if (!verify) {
        return;
    }
    $.ajax({
        cache: false,
        type: 'post',
        dataType: 'json',
        url: update_email_url,
        data: $('#jsChangeEmailForm').serialize(),
        async: true,
        beforeSend: function () {
            $btn.val("发送中...");
            $btn.attr('disabled', true);
            $("#jsChangeEmailTips").html("验证中...").show(500);
        },
        success: function (data) {
            if (data.email) {
                Dml.fun.showValidateError($('#jsChangeEmail'), data.email);
            } else if (data.status === "success") {
                setTimeout(function () {
                    location.reload();
                }, 1000);
            } else if (data.status === 'failure') {
                Dml.fun.showValidateError($('#jsChangeEmail'), "邮箱信息更新失败，验证码不正确");
            }
        },
        complete: function () {
            $btn.val("完成");
            $btn.removeAttr("disabled");
        }
    });
}

$(function () {
    //个人资料修改密码
    $('#jsUserResetPwd').on('click', function () {
        Dml.fun.showDialog('#jsResetDialog', '#jsResetPwdTips');
    });

    $('#jsResetPwdBtn').click(function () {
        $.ajax({
            cache: false,
            type: "POST",
            dataType: 'json',
            url: resetpwd_url,
            data: $('#jsResetPwdForm').serialize(),
            async: true,
            success: function (data) {
                if (data.status === "success") {
                    Dml.fun.showTipsDialog({
                        title: '提交成功',
                        h2: '修改密码成功，请重新登录!',
                    });
                    Dml.fun.winReload();
                } else if (data.msg) {
                    Dml.fun.showValidateError($("#pwd"), data.msg);
                    Dml.fun.showValidateError($("#repwd"), data.msg);
                }
            }
        });
    });

    //个人资料头像
    $('.js-img-up').uploadPreview({
        Img: ".js-img-show", Width: 94, Height: 94, Callback: function () {
            $('#jsAvatarForm').submit();
        }
    });


    $('.changeemai_btn').click(function () {
        Dml.fun.showDialog('#jsChangeEmailDialog', '#jsChangePhoneTips', 'jsChangeEmailTips');
    });
    $('#jsChangeEmailCodeBtn').on('click', function () {
        sendCodeChangeEmail($(this));
    });
    $('#jsChangeEmailBtn').on('click', function () {
        changeEmailSubmit($(this));
    });


    //input获得焦点样式
    $('.perinform input[type=text]').focus(function () {
        $(this).parent('li').addClass('focus');
    });
    $('.perinform input[type=text]').blur(function () {
        $(this).parent('li').removeClass('focus');
    });

    laydate({
        elem: '#birthday',
        format: 'YYYY-MM-DD',
        max: laydate.now()
    });

    verify(
        [
            {id: '#nick_name', tips: Dml.Msg.epNickName, require: true}
        ]
    );
    //保存个人资料
    $('#jsEditUserBtn').on('click', function () {
        var _self = $(this),
            $jsEditUserForm = $('#jsEditUserForm')
        verify = verifySubmit(
            [
                {id: '#nickname', tips: Dml.Msg.epNickName, require: true}
            ]
        );
        if (!verify) {
            return;
        }
        $.ajax({
            cache: false,
            type: 'post',
            dataType: 'json',
            url: user_info_url,
            data: $jsEditUserForm.serialize(),
            async: true,
            beforeSend: function (XMLHttpRequest) {
                _self.val("保存中...");
                _self.attr('disabled', true);
            },
            success: function (data) {
                if (data.nickname) {
                    _showValidateError($('#nickname'), data.nickname);
                } else if (data.birthday) {
                    _showValidateError($('#birthday'), data.birthday);
                } else if (data.address) {
                    _showValidateError($('#address'), data.address);
                } else if (data.status === "failure") {
                    Dml.fun.showTipsDialog({
                        title: '保存失败',
                        h2: data.msg
                    });
                } else if (data.status === "success") {
                    Dml.fun.showTipsDialog({
                        title: '保存成功',
                        h2: '个人信息修改成功！'
                    });
                    setTimeout(function () {
                        window.location.href = window.location.href;
                    }, 1500);
                }
            },
            complete: function (XMLHttpRequest) {
                _self.val("保存");
                _self.removeAttr("disabled");
            }
        });
    });


});