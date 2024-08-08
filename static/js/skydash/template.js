(function ($) {
    'use strict';
    $(function () {
        var body = $('body');
        var contentWrapper = $('.content-wrapper');
        var scroller = $('.container-scroller');
        var footer = $('.footer');
        var sidebar = $('.sidebar');

        //Add active class to nav-link based on url dynamically
        //Active class can be hard coded directly in html file also as required

        function addActiveClass() {
            $('.active').removeClass('active');
            let inp = window.location.pathname;
            console.log(inp.slice('/'));
            if (/^\/app\/users\/.*$/.test(inp)) {
                $('#nav-2').addClass('active');
            } else if (/^\/app\/permissions\/.*$/.test(inp)) {
                $('#nav-7').addClass('active');
            } else if (/^\/app\/demonstrator\/.*$/.test(inp)) {
                $('#nav-4').addClass('active');
            } else {
                switch (inp) {
                    case '/app/':
                        $('#nav-1').addClass('active');
                        break;
                    case '/app/register/':
                        $('#nav-2').addClass('active');
                        break;
                    case '/app/insert/':
                        $('#nav-3').addClass('active');
                        break;
                    case '/app/allDemonstrators/':
                        $('#nav-4').addClass('active');
                        break;
                    case '/app/gett/':
                    case '/app/query/':
                    case '/app/sendEmails/':
                        $('#nav-5').addClass('active');
                        break;
                    case '/app/send/':
                        $('#nav-6').addClass('active');
                        break;
                    case '/app/about-us':
                        $('#nav-8').addClass('active');
                        break;
                    default:
                        $('#nav-1').addClass('active');
                }
            }
        }
        addActiveClass();
        var current = location.pathname
            .split('/')
            .slice(-1)[0]
            .replace(/^\/|\/$/g, '');
        // $('.nav li a', sidebar).each(function () {
        //     var $this = $(this);
        //     addActiveClass($this);
        // });

        // $('.horizontal-menu .nav li a').each(function () {
        //     var $this = $(this);
        //     addActiveClass($this);
        // });

        //Close other submenu in sidebar on opening any

        sidebar.on('show.bs.collapse', '.collapse', function () {
            sidebar.find('.collapse.show').collapse('hide');
        });

        //Change sidebar and content-wrapper height
        applyStyles();

        function applyStyles() {
            //Applying perfect scrollbar
            if (!body.hasClass('rtl')) {
                if (
                    $('.settings-panel .tab-content .tab-pane.scroll-wrapper')
                        .length
                ) {
                    const settingsPanelScroll = new PerfectScrollbar(
                        '.settings-panel .tab-content .tab-pane.scroll-wrapper'
                    );
                }
                if ($('.chats').length) {
                    const chatsScroll = new PerfectScrollbar('.chats');
                }
                if (body.hasClass('sidebar-fixed')) {
                    if ($('#sidebar').length) {
                        var fixedSidebarScroll = new PerfectScrollbar(
                            '#sidebar .nav'
                        );
                    }
                }
            }
        }

        $('[data-toggle="minimize"]').on('click', function () {
            if (
                body.hasClass('sidebar-toggle-display') ||
                body.hasClass('sidebar-absolute')
            ) {
                body.toggleClass('sidebar-hidden');
            } else {
                body.toggleClass('sidebar-icon-only');
            }
        });

        //checkbox and radios
        $('.form-check label,.form-radio label').append(
            '<i class="input-helper"></i>'
        );

        //Horizontal menu in mobile
        $('[data-toggle="horizontal-menu-toggle"]').on('click', function () {
            $('.horizontal-menu .bottom-navbar').toggleClass('header-toggled');
        });
        // Horizontal menu navigation in mobile menu on click
        var navItemClicked = $('.horizontal-menu .page-navigation >.nav-item');
        navItemClicked.on('click', function (event) {
            if (window.matchMedia('(max-width: 991px)').matches) {
                if (!$(this).hasClass('show-submenu')) {
                    navItemClicked.removeClass('show-submenu');
                }
                $(this).toggleClass('show-submenu');
            }
        });

        $(window).scroll(function () {
            if (window.matchMedia('(min-width: 992px)').matches) {
                var header = $('.horizontal-menu');
                if ($(window).scrollTop() >= 70) {
                    $(header).addClass('fixed-on-scroll');
                } else {
                    $(header).removeClass('fixed-on-scroll');
                }
            }
        });
    });

    // focus input when clicking on search icon
    $('#navbar-search-icon').click(function () {
        $('#navbar-search-input').focus();
    });
})(jQuery);
