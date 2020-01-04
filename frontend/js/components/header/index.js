//IMPORT EXTERNAL COMPONENTS================================================
import React, { Fragment, memo } from "react";
import { Container, Menu, Responsive } from "semantic-ui-react";

// //IMPORT INTERNAL COMPONENTS================================================
import CategoriesItem from "./categories-item";
import LogoItem from "./logo-item";
import SearchItem from "./search-item";
import UserItem from "./user-item";
import CartItem from "./cart-item";

// //IMPORT EXTERNAL FUNCTIONS=================================================
import { css } from "emotion";

// //STYLE CLASSES DEFINITION==================================================
const headerClass = css({
    "&&&&&": {
        background: "lightskyblue",
        border: "1px solid rgba(34,36,38,.15)",
        boxShadow: "0 1px 2px 0 rgba(34,36,38,.15)",
        borderRadius: ".28571429rem",
        marginBottom: "3px"
    }
})

const menuClass = css({
    "&&&&&": {
        background: "lightskyblue",
        border: "0",
        boxShadow: "0",
        borderRadius: "0",
        margin: "0",
    }
})

//COMPONENT=================================================================
function Header() {
    return (
        <Container className={headerClass} fluid>
            <Menu className={menuClass} borderless>
                <CategoriesItem />
                <LogoItem />
                <Responsive
                    as={Fragment}
                    minWidth={Responsive.onlyTablet.minWidth}
                >
                    <SearchItem />
                </Responsive>
                <Menu.Menu position="right">
                    <UserItem />
                    <CartItem />
                </Menu.Menu>
            </Menu>
            <Responsive
                {...Responsive.onlyMobile}
                as={Fragment}
            >
                <Menu className={menuClass} borderless>
                    <SearchItem />
                </Menu>
            </Responsive>
        </Container>
    )
}

//EXPORT COMPONENT==========================================================
export default memo(Header);