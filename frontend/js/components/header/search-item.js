//IMPORT EXTERNAL COMPONENTS================================================
import React, { useState, useEffect } from "react";
import { withRouter } from "react-router-dom";
import { Menu, Form, Input, Button } from "semantic-ui-react";

// //IMPORT EXTERNAL FUNCTIONS=================================================
import { css } from "emotion";

// //STYLE CLASSES DEFINITION==================================================
const itemClass = css({
    "&&&&&, &&&&&>.form": {
        flexGrow: 1
    }
})

//COMPONENT=================================================================
function SearchItem({ history, location }) {
    const [searchquery, setSearchQuery] = useState("");

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
export default withRouter(SearchItem);