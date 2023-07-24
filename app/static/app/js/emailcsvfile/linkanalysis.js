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
                edges.forEach(function(d) {
                  d.count = + d.count; // Chuyển đổi giá trị count sang kiểu số
                });

              var simulation = d3.forceSimulation(nodes)
              .force("link", d3.forceLink(edges).id(function(d) { return d.id; }).distance(200)) // Thay đổi giá trị distance
              .force("charge", d3.forceManyBody().strength(-3500))
              .force("center", d3.forceCenter(width / 2, height / 2))
              .force("x", d3.forceX(width / 2).strength(0.3)) // Giới hạn vị trí x của các node trong khung
              .force("y", d3.forceY(height / 2).strength(0.5)); // Giới hạn vị trí y của các node trong khung

              simulation.on("tick", function() {
                // Cập nhật vị trí của các cạnh và nút dựa trên thông tin của simulation
                link.attr("x1", function(d) { return d.source.x; })
                  .attr("y1", function(d) { return d.source.y; })
                  .attr("x2", function(d) { return d.target.x; })
                  .attr("y2", function(d) { return d.target.y; });
                text_count.attr("x", function(d) { return (d.source.x + d.target.x) /2; })
                  .attr("y", function(d) { return (d.source.y+d.target.y)/2; });
                circle_text.attr("cx", function(d) { return (d.source.x + d.target.x) /2; })
                  .attr("cy", function(d) { return (d.source.y+d.target.y)/2; });
                // Cập nhật vị trí của các node và text
                node.attr("transform", function(d) { return "translate(" + d.x + "," + d.y + ")"; });
              });

              // Tạo một phần tử <g> để nhóm <line> và <text>
                var linkGroup = svg.selectAll(".link-group")
                .data(edges)
                .enter()
                .append("g")
                .attr("class", "link-group");
                // Vẽ cạnh (line)
                var link = linkGroup.append("line")
                  .attr("class", "link")
                  .style("stroke", "gray")
                  .style("stroke-width", 1);
                var circle_text = linkGroup.append("circle")
                  .attr("class", "count-circle")
                  .style("fill", "blue") // Đổi màu của hình tròn
                  .attr("r", 10); // Đặt bán kính của hình tròn
                var text_count = linkGroup.append("text")
                  .attr("class", "counttext")
                  .style("text-anchor", "middle") // Căn giữa theo trục x
                  .style("dominant-baseline", "middle") // Căn giữa theo trục y
                  .style("font-weight", "bold") // Đặt độ đậm
                  .style("font-size", "12px") // Đặt kích thước
                  .style("fill", "white") 
                  .text(function(d) { return d.count; });

              // Vẽ nút (nodes)
              var node = svg.selectAll(".node")
                .data(nodes)
                .enter()
                .append("g")
                .attr("class", "node");
              
              // Vẽ hình tròn cho mỗi node
              node.append("image")
                .attr("xlink:href", personImageUrl)  // Đường dẫn đến hình ảnh của người
                .attr("x", -10)  // Đặt vị trí x của hình ảnh
                .attr("y", -10)  // Đặt vị trí y của hình ảnh
                .attr("width", 40)  // Đặt chiều rộng của hình ảnh
                .attr("height", 40);  // Đặt chiều cao của hình ảnh
                
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

