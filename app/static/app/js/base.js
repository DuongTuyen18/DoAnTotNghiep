// function handleCSVFile(event) {
//   var file = event.target.files[0];
//   if (file) {
//     // Xử lý tệp CSV tại đây, ví dụ:
//     var reader = new FileReader();
//     reader.onload = function(e) {
//       var contents = e.target.result;
//       // Xử lý nội dung tệp CSV ở đây
//       console.log(contents);
//     };
//     reader.readAsText(file);
//   }
// }
$(document).ready(function () {


  // Lắng nghe sự kiện click vào thẻ a
document.getElementById('ChooseFolderEML').addEventListener('click', function (event) {
  // Ngăn chặn hành động mặc định của thẻ a
  event.preventDefault();
  
  // Tạo input element và sử dụng thuộc tính webkitdirectory để cho phép chọn thư mục
  var input = document.createElement('input');
  input.setAttribute('type', 'file');
  input.setAttribute('webkitdirectory', true);
  
  // Lắng nghe sự kiện onchange của input để lấy đường dẫn của thư mục đã chọn
  input.addEventListener('change', function (event) {
    // Lấy đường dẫn của thư mục đầu tiên đã chọn
    // Lấy phần tử input có kiểu file
    var input = document.getElementById('folder');

    // Xóa bỏ giá trị hiện tại của phần tử input
    input.value = '';

    // Thêm các tệp được chọn vào phần tử input
    input.files = event.target.files;
    const selectedFolder = event.target.files[0].webkitRelativePath;
    const folderName = selectedFolder.split('/')[0];
    $("#folder_name").val(folderName);
    // Gửi form đi để xử lý đường dẫn thư mục đã chọn trong Django
    document.getElementById('chooseFolderForm').submit();
  });
  
  // Kích hoạt sự kiện click cho input để mở dialog chọn thư mục
  input.click();
});
document.getElementById('Choosefile_csv').addEventListener('click', function (event) {
  debugger
  // Ngăn chặn hành động mặc định của thẻ a
  event.preventDefault();
  
  // Tạo input element và sử dụng thuộc tính webkitdirectory để cho phép chọn thư mục
  var input = document.createElement('input');
  input.setAttribute('type', 'file');
  // Lắng nghe sự kiện onchange của input để lấy đường dẫn của thư mục đã chọn
  input.addEventListener('change', function (event) {
    // Lấy đường dẫn của thư mục đầu tiên đã chọn
    // Lấy phần tử input có kiểu file
    var input = document.getElementById('csv_file_input');

    // Xóa bỏ giá trị hiện tại của phần tử input
    input.value = '';

    // Thêm các tệp được chọn vào phần tử input
    input.files = event.target.files;
    // Gửi form đi để xử lý đường dẫn thư mục đã chọn trong Django
    document.getElementById('choosefile_csv_form').submit();
  });
  
  // Kích hoạt sự kiện click cho input để mở dialog chọn thư mục
  input.click();
});
// $('#ChooseFolderEML').on('click', function(event) {
//   // Ngăn chặn hành động mặc định của thẻ a
//   event.preventDefault();

//   // Tạo input element và sử dụng thuộc tính webkitdirectory để cho phép chọn thư mục
//   var input = $('<input type="file" webkitdirectory />');

//   // Lắng nghe sự kiện onchange của input để lấy đường dẫn của thư mục đã chọn
//   input.on('change', function(event) {
//     // Lấy đường dẫn tuyệt đối của thư mục được chọn
//     var folderPath = $(this).val();
//     alert(folderPath);
//     // Đưa đường dẫn vào trường input trong form
//     $('#folderPathInput').val(folderPath);

//     // Gửi form đi để xử lý đường dẫn thư mục đã chọn trong Django
//     $('#chooseFolderForm').submit();
//   });

  // Kích hoạt sự kiện click cho input để mở dialog chọn thư mục
//   input.click();
// });
// $('#ChooseFolderEML').on('click', function() {
//   window.showDirectoryPicker().then(function(directory) {
//     var folder_path = directory.name;
//     $.ajax({
//       url: '/choosefolder/',
//       type: 'POST',
//       data: {'folder': folder_path},
//       dataType: 'json',
//       success: function(response) {
//         console.log('Đã chọn thư mục:', response.folder_path);
//       },
//       error: function(error) {
//         console.error('Lỗi:', error);
//       }
//     });
//   });
// });
  $("#list-menu-top .nav-item").click(function () {
    // Xóa class 'active' từ tất cả các mục trong danh sách
    $("#list-menu-top .nav-item").removeClass("active");
    // Thêm class 'active' vào mục được click
    $(this).addClass("active");
  });
  // $("#ChooseFolderEML").click(function () {
  //   window.folderPath = null; // Khởi tạo biến lưu đường dẫn thư mục
  //     window.showDirectoryPicker()
  //       .then(function(directory) {
  //         window.folderPath = directory; // Lưu đường dẫn thư mục vào biến
  //         $('#folder').val(window.folderPath); // Hiển thị đường dẫn thư mục lên ô input
  //         alert($('#folder').val());
  //       })
  //       .catch(function(error) {
  //         console.error(error); // In ra lỗi nếu có
  //       });
  // });
  $(".list-file-email .item-file-email").click(function () {
    localStorage.setItem("activeTab", $(this).attr("id"));
    localStorage.setItem("activeTab_menucontent", "inforemail_content");
  });

  $("#list-menu-right-content .nav-item .nav-link").click(function () {
    localStorage.setItem("activeTab_menucontent", $(this).attr("id"));
  });

  $(document).mouseup(function (e) {
    var container = $("#list-menu-top");
    // Kiểm tra xem phần tử được click có phải là thẻ li hay không
    if (!container.is(e.target) && container.has(e.target).length === 0) {
      // Nếu không phải, xóa lớp active của tất cả các thẻ li
      container.find("li").removeClass("active");
    }
  });

  $(".stopPropagation-edfDropdown").click(function (e) {
    e.stopPropagation(); // ngăn chặn sự kiện click lan ra các phần tử khác
    $(".eaDropdown ul").removeClass("show");
  });
  $(".stopPropagation-eaDropdown").click(function (e) {
    e.stopPropagation(); // ngăn chặn sự kiện click lan ra các phần tử khác
    $(".edfDropdown ul").removeClass("show");
  });
  $(".stopPropagation-emlDropdown").click(function (e) {
    e.stopPropagation(); // ngăn chặn sự kiện click lan ra các phần tử khác
    $(".msgDropdown ul").removeClass("show");
  });
  $(".stopPropagation-msgDropdown").click(function (e) {
    e.stopPropagation(); // ngăn chặn sự kiện click lan ra các phần tử khác
    $(".emlDropdown ul").removeClass("show");
  });
  $(".stopPropagation-addADropdown").click(function (e) {
    e.stopPropagation(); // ngăn chặn sự kiện click lan ra các phần tử khác
    $(".manageADropdown ul").removeClass("show");
  });
  $(".stopPropagation-manageADropdown").click(function (e) {
    e.stopPropagation(); // ngăn chặn sự kiện click lan ra các phần tử khác
    $(".addADropdown ul").removeClass("show");
  });

  
});
