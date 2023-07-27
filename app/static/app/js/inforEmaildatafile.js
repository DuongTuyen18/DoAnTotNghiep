
$(document).ready(function () {


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