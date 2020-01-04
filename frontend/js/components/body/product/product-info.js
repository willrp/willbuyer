//IMPORT EXTERNAL COMPONENTS================================================
import React from "react";
import { Link } from "react-router-dom";
import { List } from "semantic-ui-react";

//COMPONENT=================================================================
function ProductInfo({ name, brand, kind, about, care, details }) {
    function renderDetails(details) {
        let key = 0;
        return details.map(
            (item) => {
                key++;
                return (
                    item + ((key < details.length) ? "; " : "")
                )
            }
        );
    }

    function render() {
        return (
            <List>
                <List.Item>
                    <List.Header as="h2">{name}</List.Header>
                    <List.Description>
                        <Link to={`/kind/${kind}`}>{kind} </Link>by<Link to={`/brand/${brand}`}> {brand}</Link>
                    </List.Description>
                </List.Item>
                <List.Item>
                    <List.Header>About:</List.Header>
                    <List.Content>{about}</List.Content>
                </List.Item>
                <List.Item>
                    <List.Header>Care:</List.Header>
                    <List.Content>{care}</List.Content>
                </List.Item>
                <List.Item>
                    <List.Header>Details:</List.Header>
                    <List.Content>{renderDetails(details)}</List.Content>
                </List.Item>
            </List>
        )
    }

    return render()
}

//EXPORT COMPONENT==========================================================
export default ProductInfo;