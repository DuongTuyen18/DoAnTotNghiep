
$(document).ready(function () {

  // $('#list-menu-right-content .nav-item .nav-link').click(function() {
  //   localStorage.setItem('activeTab1', $(this).attr('href'));
  //   debugger

  // });

  // var activeTab1 = localStorage.getItem('activeTab1');
  // if (activeTab1) {
  //   $('#list-menu-right-content .nav-item a').removeClass('active');
  //   $('#list-menu-right-content .nav-item a[href="' + activeTab1 + '"]').addClass('active');
  // }


  var activeTab = localStorage.getItem('activeTab');
  if (activeTab) {
    $('#' + activeTab).addClass('active');
  }

  var activeTab_menucontent = localStorage.getItem('activeTab_menucontent');
  if (activeTab_menucontent) {
    $('#list-menu-right-content .nav-item a').removeClass('active');
    $('#' + activeTab_menucontent).addClass('active');
  }
})