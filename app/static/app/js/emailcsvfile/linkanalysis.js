$(document).ready(function () {

    $("#icon_select_all").click(function() {
      var isChecked = $(this).prop("checked");
      $("#left-content-list-email-linkanalysis input[type='checkbox']").prop("checked", isChecked);
    });



    $("#box-action-header").click(function(){
            // Tạo một mảng để lưu trữ danh sách email được chọn
        var selectedEmails = [];

        // Duyệt qua tất cả các checkbox
        $("#left-content-list-email-linkanalysis input[type='checkbox']").each(function() {
        // Kiểm tra nếu checkbox được chọn
          if ($(this).is(":checked")) {
              // Lấy giá trị của email tương ứng
              var email = $(this).closest(".list-group-item").find(".box-infor-file").text().trim();
              // Thêm email vào danh sách
              selectedEmails.push(email);
          }
        });
        var list_email = selectedEmails;
        console.log(list_email);
        $.ajax({
            url: "/csvdatafile/link_analysis/link_analysis_choose_email",
            type: "GET",
            data: {
                list_email: list_email
              },
            success: function(response) {

                var linkAnalysisData = JSON.parse(response);
                $("#canvas_link").html('');
                var width = $("#canvas_link").width();
                var height = $("#canvas_link").height();
                // Tạo đối tượng SVG và gán nó cho phần tử có id là "canvas"
                var svg = d3.select("#canvas_link")
                .append("svg")  
                .style("width", width)
                .style("height", height)  

                  // Xác định độ rộng và chiều cao của canvas
                var width = svg.node().clientWidth;
                var height = svg.node().clientHeight;
                // Thiết lập thông tin về đồ thị (nodes và edges) từ dữ liệu linkAnalysisData
                var nodes = linkAnalysisData.nodes;
                var edges = linkAnalysisData.links;
                

              var simulation = d3.forceSimulation(nodes)
              .force("link", d3.forceLink(edges).id(function(d) { return d.id; }).distance(200)) // Thay đổi giá trị distance
              .force("charge", d3.forceManyBody().strength(-800))
              .force("center", d3.forceCenter(width / 2, height / 2))
              .force("x", d3.forceX(width / 2).strength(0.2)) // Giới hạn vị trí x của các node trong khung
              .force("y", d3.forceY(height / 2).strength(0.2)); // Giới hạn vị trí y của các node trong khung

              simulation.on("tick", function() {
                // Cập nhật vị trí của các cạnh và nút dựa trên thông tin của simulation
                link.attr("x1", function(d) { return d.source.x; })
                  .attr("y1", function(d) { return d.source.y; })
                  .attr("x2", function(d) { return d.target.x; })
                  .attr("y2", function(d) { return d.target.y; });
              
                // Cập nhật vị trí của các node và text
                node.attr("transform", function(d) { return "translate(" + d.x + "," + d.y + ")"; });
              });

                // Vẽ cạnh (edges)
                var link = svg.selectAll(".link")
                  .data(edges)
                  .enter()
                  .append("line")
                  .attr("class", "link")
                  .style("stroke", "gray")
                  .style("stroke-width", 1);
              
              // Vẽ nút (nodes)
              var node = svg.selectAll(".node")
                .data(nodes)
                .enter()
                .append("g")
                .attr("class", "node");
              
              // Vẽ hình tròn cho mỗi node
              node.append("circle")
                .attr("r", 10)
                .style("fill", "blue");
              
              // Hiển thị tên của mỗi node
              node.append("text")
                .attr("dx", 0) // Dịch chuyển vị trí của text
                .attr("dy", -20)
                .text(function(d) { return d.id; });
              
              // Thiết lập sự kiện khi di chuyển đồ thị

            },
            error: function(xhr, errmsg, err) {
                // Xử lý lỗi nếu có
                console.log(xhr.status + ": " + xhr.responseText);
            }
        });
    })
});

