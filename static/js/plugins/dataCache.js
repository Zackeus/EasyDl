/**
 * 本地打开则会应用此文件夹内容，非本地打开则会调用 /services/data文件夹中的json文件作为数据。
 * 此文件夹建立的目的仅仅是为兼容本地直接打开，不用去安装web服务容器。
 */


/**
 * 获取用户信息
 */
function getJson_getUserInfo() {
    var obj = {
        code: 200,
        token: "taVJM3Ba3lBTr/LSsoiAsv+Qd2Qt8j4d",
        msg: null,
        data: [
            {
                user_acc: "admin",
                user_name: "admin",
                passwd: "c3284d0f94606de1fd2af172aba15bf3",
                icon: "/images/face.jpg",
                mobile: "13474824061",
                tel_phone: "4000820099",
                e_mail: "1567174Q@qq.com",
                create_time: "2017-02-08T00:00:00",
                create_user: "system",
                is_lock: 1,
                roleNames: [
                    "超级管理员(不受权限模块限制,永远拥有所有权限.)"
                ]
            }
        ]
    };
    return obj;
}

/**
 * 获取所有菜单
 */
function getJson_menu() {
    var obj = {
        "code": 200,
        "token": "taVJM3Ba3lD/YmU19m1VLj9BrBMs8CdS",
        "msg": null,
        "data": [
            {
                "title": "主页",
                "icon": "&#xe68e;",
                "href": "/pages/main/main.html",
                "children": []
            },
            {
                "title": "网站管理",
                "icon": "&#xe7ae;",
                "href": "",
                "children": [
                    {
                        "title": "栏目管理",
                        "icon": "",
                        "href": "pages/webAdmin/column.html",
                        "children": []
                    },
                    {
                        "title": "内容管理",
                        "icon": "&#xe638;",
                        "href": "pages/webAdmin/content.html",
                        "children": []
                    },
                    {
                        "title": "广告管理",
                        "icon": "layui-icon-survey",
                        "href": "pages/webAdmin/advertisement.html",
                        "children": []
                    },
                    {
                        "title": "三级菜单",
                        "icon": "",
                        "href": "pages/webAdmin/advertisement.html",
                        "children": [
                            {
                                "title": "三级菜单之一",
                                "icon": "",
                                "href": "pages/webAdmin/advertisement.html",
                                "children": []
                            },
                            {
                                "title": "三级菜单之二",
                                "icon": "",
                                "href": "pages/webAdmin/advertisement.html",
                                "children": []
                            }
                        ]
                    },
                    {
                        "title": "支持无限极菜单",
                        "icon": "",
                        "href": "pages/webAdmin/advertisement.html",
                        "children": [
                            {
                                "title": "三级菜单之一2",
                                "icon": "",
                                "href": "pages/webAdmin/advertisement.html",
                                "children": []
                            },
                            {
                                "title": "三级菜单之二2",
                                "icon": "",
                                "href": "pages/webAdmin/advertisement.html",
                                "children": []
                            },
                            {
                                "title": "四级菜单2",
                                "icon": "",
                                "href": "pages/webAdmin/advertisement.html",
                                "children": [
                                    {
                                        "title": "四级菜单之 一",
                                        "icon": "",
                                        "href": "pages/webAdmin/advertisement.html",
                                        "children": []
                                    },
                                    {
                                        "title": "五级菜单",
                                        "icon": "",
                                        "href": "pages/webAdmin/advertisement.html",
                                        "children": [
                                            {
                                                "title": "五级菜单之 一",
                                                "icon": "",
                                                "href": "pages/webAdmin/advertisement.html",
                                                "children": []
                                            },
                                            {
                                                "title": "六级菜单",
                                                "icon": "",
                                                "href": "pages/webAdmin/advertisement.html",
                                                "children": [
                                                    {
                                                        "title": "六级菜单之 一",
                                                        "icon": "",
                                                        "href": "pages/webAdmin/advertisement.html",
                                                        "children": []
                                                    },
                                                    {
                                                        "title": "六级菜单之 二",
                                                        "icon": "",
                                                        "href": "pages/webAdmin/advertisement.html",
                                                        "children": []
                                                    }
                                                ]
                                            }
                                        ]
                                    }
                                ]
                            }
                        ]
                    }
                ]
            },
            {
                "title": "用户权限",
                "icon": "&#xe672;",
                "href": "",
                "children": [
                    {
                        "title": "用户管理",
                        "icon": "&#xe612;",
                        "href": "pages/userRights/user.html",
                        "children": []
                    },
                    {
                        "title": "权限设置",
                        "icon": "&#xe60a;",
                        "href": "pages/userRights/power.html",
                        "children": []
                    },
                    {
                        "title": "角色管理",
                        "icon": "&#xe613;",
                        "href": "pages/userRights/role.html",
                        "children": []
                    },
                    {
                        "title": "菜单管理",
                        "icon": "&#xe62a;",
                        "href": "pages/userRights/menu.html",
                        "children": []
                    }
                ]
            },
            {
                "title": "系统设置",
                "icon": "&#xe614;",
                "href": "",
                "children": [
                    {
                        "title": "基本信息",
                        "icon": "&#xe647;",
                        "href": "pages/sysSetup/basicData.html",
                        "children": []
                    },
                    {
                        "title": "数据清理",
                        "icon": "&#xe640;",
                        "href": "pages/sysSetup/dataClear.html",
                        "children": []
                    },
                    {
                        "title": "SEO优化",
                        "icon": "&#xe630;",
                        "href": "pages/sysSetup/seoOptimize.html",
                        "children": []
                    },
                    {
                        "title": "友情链接",
                        "icon": "&#xe62e;",
                        "href": "pages/sysSetup/friendshipLink.html",
                        "children": []
                    },
                    {
                        "title": "模板管理",
                        "icon": "&#xe663;",
                        "href": "pages/sysSetup/templateAdmin.html",
                        "children": []
                    }
                ]
            },
            {
                "title": "报表",
                "icon": "&#xe637;",
                "href": "",
                "children": [
                    {
                        "title": "用户统计",
                        "icon": "&#xe629;",
                        "href": "pages/reportForm/statistics.html",
                        "children": []
                    },
                    {
                        "title": "日志报表",
                        "icon": "&#xe62a;",
                        "href": "pages/reportForm/log.html",
                        "children": []
                    }
                ]
            },
            {
                "title": "其他",
                "icon": null,
                "href": "",
                "children": [
                    {
                        "title": "404-新页面跳转",
                        "icon": null,
                        "href": "pages/404.html",
                        "target": "_blank",
                        "children": []
                    },
                    {
                        "title": "登录-当前页跳转",
                        "icon": null,
                        "href": "login.html",
                        "target": "_self",
                        "children": []
                    },
                    {
                        "title": "登录2-当前页跳转",
                        "icon": null,
                        "href": "pages/login/login2.html",
                        "target": "_top",
                        "children": []
                    }
                ]
            }
        ]
    };
    return obj;
}

/**
 * 获取代办
 */
function getJson_todayQuery() {
    var obj = {
        code: 200,
        token: "taVJM3Ba3lD/YmU19m1VLpkPddvGO8jA",
        msg: null,
        statusCode: null,
        data: [
            {
                "value": 335,
                "name": "直接访问"
            },
            {
                "value": 310,
                "name": "邮件营销"
            },
            {
                "value": 234,
                "name": "联盟广告"
            },
            {
                "value": 135,
                "name": "视频广告"
            },
            {
                "value": 1548,
                "name": "搜索引擎"
            }
        ]
    };
    return obj;
}

/**
 * 获取代办表格
 */
function getJson_todayUserTable() {
    var obj = {
        "code": 200,
        "msg": "",
        "count": 1000,
        "data": [
            {
                "id": 10000,
                "area": "北京"
            },
            {
                "id": 10001,
                "area": "上海"
            },
            {
                "id": 10002,
                "area": "广州"
            },
            {
                "id": 10003,
                "area": "深圳"
            },
            {
                "id": 10004,
                "area": "长沙"
            },
            {
                "id": 10005,
                "area": "株洲"
            },
            {
                "id": 10006,
                "area": "重庆"
            },
            {
                "id": 10007,
                "area": "东莞"
            }
        ]
    };
    return obj;
}

/**
 * 代办集合
 */
function getJson_todoList() {
    var obj = {
        "code": 200,
        "token": "taVJM3Ba3lD/YmU19m1VLtIH6oNNji/F",
        "msg": null,
        "statusCode": null,
        "data": [{
            "name": "todo_ocrerr",
            "value": "0"
        }, {
            "name": "todo_conflict",
            "value": "1"
        }, {
            "name": "todo_checkerr",
            "value": "0"
        }, {
            "name": "todo_matcherr",
            "value": "1"
        }, {
            "name": "todo_posterr",
            "value": "1"
        }, {
            "name": "no_match_bill",
            "value": "0"
        }, {
            "name": "todo_comp_null",
            "value": "0"
        }, {
            "name": "todo_no_match",
            "value": "2"
        }]
    };
    return obj;
}

/**
 * 图片是否上传成功
 */
function getJson_userImgUpload() {
    var obj = {
        "code": 200,
        "token": "taVJM3Ba3lCjWWUkVK//vNFwbxno/Lvq",
        "msg": null,
        "data": null
    }
    return obj;
}