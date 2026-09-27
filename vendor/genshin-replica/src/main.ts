import "@alphardex/aqua.css/dist/aqua.min.css";
import "./style.css";

import { adaptMobileDOM } from "kokomi.js";

import Experience from "./Experience/Experience";
import { replicaConfig } from "./replicaConfig";

document.querySelector<HTMLDivElement>("#app")!.innerHTML = /* html */ `
<div id="sketch"></div>
<div class="loader-screen fixed z-5 top-0 left-0 w-full h-full bg-white transition-opacity"
  style="transition-duration: 1.5s;">
  <div class="absolute hv-center">
    <div class="flex flex-col items-center space-y-6">
      <img src="./Genshin/Genshin.png" class="title block" style="width: 45vmin;" alt="" />
      <progress class="loader-progress progress-bar" value="0" max="100"></progress>
    </div>
  </div>
</div>
<div class="menu fixed z-4 top-0 left-0 w-full h-full select-none hidden pointer-events-none">
  <div class="menu-content transition-opacity duration-1000">
    <div class="disclaimer">
      <p>免责声明：</p>
      <p>
        本网站是一个纯粹的技术示例，旨在展示和分享我们的技术能力。网站的设计和内容受到《原神》的启发，并尽可能地复制了《原神》的登录界面。我们对此表示敬意，并强调这个项目不是官方的《原神》产品，也没有与《原神》或其母公司miHoYo有任何关联。
      </p>
      <p>
        我们没有，也无意从这个项目中获得任何经济利益。这个网站的所有内容仅供学习和研究目的，以便让更多的人了解和熟悉webgl开发技术。
      </p>
      <p>如果miHoYo或任何有关方面认为这个项目侵犯了他们的权益，请联系我们，我们会立即采取行动。</p>
    </div>
  </div>
</div>
<div class="loading-element fixed z-4 top-0 left-0 w-full h-full bg-white select-none overflow-hidden hollow">
  <div class="absolute hv-center">
    <div class="loading-element-wrapper">
      <img src="./Genshin/Elements.png" class="loading-element-img" alt="" />
    </div>
  </div>
</div>
`;

const app = document.querySelector("#app")! as HTMLElement;

adaptMobileDOM(app);
window.addEventListener("resize", () => {
  adaptMobileDOM(app);
});

const cfg = replicaConfig();
if (cfg.disclaimer) {
  const box = document.querySelector(".disclaimer");
  if (box) {
    box.innerHTML = cfg.disclaimer
      .split(/\n+/)
      .map((line) => `<p>${line.replace(/[&<>]/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;" }[c] as string))}</p>`)
      .join("");
  }
}

new Experience("#sketch");
