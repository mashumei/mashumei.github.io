/* 马树梅 · 鸿雁归巢 个人AI名片网站 —— 交互脚本 */
(function () {
  "use strict";

  var burger = document.querySelector(".hamburger");
  var menu = document.querySelector(".mobile-menu");
  var navLinks = document.querySelectorAll(".mobile-menu a");

  function closeMenu() {
    if (burger) burger.classList.remove("open");
    if (menu) menu.classList.remove("open");
  }

  if (burger && menu) {
    burger.addEventListener("click", function () {
      var open = burger.classList.toggle("open");
      menu.classList.toggle("open", open);
    });
    navLinks.forEach(function (a) {
      a.addEventListener("click", closeMenu);
    });
  }

  /* 滚动时高亮当前栏目（桌面端导航） */
  var sections = document.querySelectorAll("section[id]");
  var desktopLinks = document.querySelectorAll(".nav-links a");

  if ("IntersectionObserver" in window && sections.length && desktopLinks.length) {
    var observer = new IntersectionObserver(
      function (entries) {
        entries.forEach(function (entry) {
          if (entry.isIntersecting) {
            var id = entry.target.getAttribute("id");
            desktopLinks.forEach(function (l) {
              l.classList.toggle("active", l.getAttribute("href") === "#" + id);
            });
          }
        });
      },
      { rootMargin: "-45% 0px -50% 0px", threshold: 0 }
    );
    sections.forEach(function (s) { observer.observe(s); });
  }

  /* 复制文本（如电话号码）：复制并给出反馈 */
  document.querySelectorAll("[data-copy]").forEach(function (btn) {
    btn.addEventListener("click", function () {
      var text = btn.getAttribute("data-copy");
      if (!text || text.indexOf("待填写") !== -1) {
        alert("内容尚未填写，请先在 index.html 中补充。");
        return;
      }
      var old = btn.textContent;
      var done = function () {
        btn.textContent = "已复制 ✓";
        setTimeout(function () { btn.textContent = old; }, 1500);
      };
      if (navigator.clipboard && navigator.clipboard.writeText) {
        navigator.clipboard.writeText(text).then(done, done);
      } else {
        var ta = document.createElement("textarea");
        ta.value = text;
        document.body.appendChild(ta);
        ta.select();
        try { document.execCommand("copy"); } catch (e) {}
        document.body.removeChild(ta);
        done();
      }
    });
  });

  /* 拨打电话（占位，待补充真实号码后生效） */
  var callBtn = document.querySelector("[data-call-phone]");
  if (callBtn) {
    callBtn.addEventListener("click", function () {
      var num = callBtn.getAttribute("data-call-phone");
      if (!num || num.indexOf("待填写") !== -1) {
        alert("电话尚未填写，请先在 index.html 中补充真实号码。");
        return;
      }
      window.location.href = "tel:" + num;
    });
  }

})();
