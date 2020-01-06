//IMPORT EXTERNAL COMPONENTS================================================
import React, { useContext } from "react";
import { useLocation } from "react-router";
import { Link } from "react-router-dom";
import { Menu, Dropdown, Icon, Image, Label } from "semantic-ui-react";

//IMPORT CONTEXTS===========================================================
import { CurrentUserContext } from "contexts/current-user-context";

// //IMPORT EXTERNAL FUNCTIONS=================================================
import { css } from "emotion";

// //STYLE CLASSES DEFINITION==================================================
const itemClass = css({
    "&&&&&:hover": {
        backgroundColor: "deepskyblue"
    }
})

const menuClass = css({
    "&&&&& .header": {
        paddingLeft: "0.5em",
        paddingRight: "0.1em",
        margin: "0",
        marginTop: "0.5em"
        
    },
    "&&&&& .label": {
        display: "flex",
        flexGrow: 1,
        paddingLeft: "0",
        paddingRight: "2.5em",
        color: "black",
        backgroundColor: "lightskyblue"
    }
})

//COMPONENT=================================================================
function UserItem() {
    const { data, isLoggedIn } = useContext(CurrentUserContext);
    const { pathname, state } = useLocation();

    function renderLogin() {
        var redirVar = "?next=" + pathname;

        if(typeof state !== "undefined" && "from" in state){
            redirVar = "?next=" + state.from.pathname;
        }
        else if(pathname === "/login" || pathname === "/"){
            redirVar = "";
        }

        return (
            <Menu.Item
                as="a"
                href={"/auth/login" + redirVar}
                className={itemClass}
            >
                <Icon name="sign in" />Log in
            </Menu.Item>
        )
    }

    function renderLogout() {
        const { name, picture } = data;

        return (
            <Menu.Item
                as={Dropdown}
                position="right"
                className={itemClass}
                trigger={<span><Icon name="user" />User Panel</span>}
            >
                <Dropdown.Menu className={menuClass}>
                    <Dropdown.Header>
                        <Label image>
                            <Image src={picture} alt=" " />
                            {name}
                        </Label>
                    </Dropdown.Header>
                    <Dropdown.Divider />
                    <Dropdown.Item as={Link} to="/orders" icon="shopping basket" text="Orders" />
                    <Dropdown.Item as="a" href="/auth/logout" icon="sign out" text="Logout" />
                </Dropdown.Menu>
            </Menu.Item>
        )
    }

    function render() {
        if(isLoggedIn) {
            return renderLogout()
        }
        else{
            return renderLogin()
        }
    }

    return (
        render()
    )
}

//EXPORT COMPONENT==========================================================
export default UserItem;