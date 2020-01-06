//IMPORT EXTERNAL COMPONENTS================================================
import React, { useState, useEffect } from "react";
import { useLocation } from "react-router";
import { useHistory } from "react-router-dom";
import { Menu, Form, Button } from "semantic-ui-react";

// //IMPORT EXTERNAL FUNCTIONS=================================================
import { css } from "emotion";

// //STYLE CLASSES DEFINITION==================================================
const itemClass = css({
    "&&&&&, &&&&&>.form": {
        flexGrow: 1
    }
})

//COMPONENT=================================================================
function SearchItem() {
    const [searchquery, setSearchQuery] = useState("");
    let history = useHistory();
    const location = useLocation();

    useEffect(() => {
        setSearchQuery("");
    }, [location.key])

    function onInputChange(e, { value }) {
        setSearchQuery(value);
    }

    function onSearchSubmit() {
        if(searchquery !== "") {
            history.push(`/search/${searchquery}`);
        }
    }

    return (
        <Menu.Item className={itemClass}>
            <Form onSubmit={onSearchSubmit}>
                <Form.Input
                    type="text"
                    placeholder="Search"
                    fluid
                    onChange={onInputChange}
                    value={searchquery}
                    action
                >
                    <input />
                    <Button icon="search" type="submit" />
                </Form.Input>
            </Form>
        </Menu.Item>
    )
}

//EXPORT COMPONENT==========================================================
export default SearchItem;