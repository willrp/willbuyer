//IMPORT EXTERNAL COMPONENTS================================================
import React from "react";
import { Link } from "react-router-dom";
import { Menu, Image } from "semantic-ui-react";

//IMPORT INTERNAL ASSETS====================================================
import menulogo from "img/intrologo.png";

//IMPORT EXTERNAL FUNCTIONS=================================================
import { css } from "emotion";

//STYLE CLASSES DEFINITION==================================================
const itemClass = css({
    "&&&&:hover": {
        backgroundColor: "lightskyblue"
    }
})

const imgClass = css({
    "&&&&": {
        width: "auto",
        minHeight: "4em",
        maxHeight: "4.7em"
    }
})

//COMPONENT=================================================================
function LogoItem() {
    return (
        <Menu.Item
            as={Link}
            to="/"
            className={itemClass}
            fitted
        >
            <Image src={menulogo} className={imgClass} />
        </Menu.Item>
    )
}

//EXPORT COMPONENT==========================================================
export default LogoItem;