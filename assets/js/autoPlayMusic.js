$(document).ready(function() {
   // Lấy thẻ audio
   var nhacNen = document.getElementById('nhacNen');

   // Bắt sự kiện click vào toàn bộ body
   $('body').one('click', function() {
     // Phát nhạc khi người dùng click vào trang
     nhacNen.play();
     nhacNen.loop = true;
     console.log("Nhạc đang phát");
   });
 });