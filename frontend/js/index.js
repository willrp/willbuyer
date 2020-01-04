//IMPORT ASSETS=============================================================
import "img/favicon.ico";
import "img/intrologo.png";
import "img/loading.gif";
import "css/reset.css";
import "react-nprogress/nprogress.css";;
import "react-toastify/dist/ReactToastify.css";
import "slick-carousel/slick/slick.css";
import "slick-carousel/slick/slick-theme.css";
import "rc-slider/assets/index.css";
import "react-image-gallery/styles/css/image-gallery.css";
import "semantic-ui-css/semantic.min.css";
import "react-dates/initialize";
import "react-dates/lib/css/_datepicker.css";
import "css/style.css";

//IMPORT EXTERNAL COMPONENTS================================================
import React from "react";

//IMPORT EXTERNAL FUNCTIONS=================================================
import { render } from "react-dom";

//IMPORT INTERNAL COMPONENTS================================================
import Root from "components/root";

//COMPONENT=================================================================
const root = document.getElementById("root");
if (!root) {
    throw new Error("couldn't find element with id root")
}

render(
    <Root />,
    root
)