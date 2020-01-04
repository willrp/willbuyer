//IMPORT EXTERNAL COMPONENTS================================================
import React, { Fragment, useState, useContext, useEffect, useReducer } from "react";
import { Link } from "react-router-dom";
import { Button, Icon, Modal, Message } from "semantic-ui-react";

//IMPORT CONTEXTS===========================================================
import { CartContext } from "contexts/cart-context";
import { CurrentUserContext } from "contexts/current-user-context";

//IMPORT HOOKS==============================================================
import useRequestData from "hooks/request-data";

//IMPORT EXTERNAL FUNCTIONS=================================================
import { css } from "emotion";

//STYLE CLASSES DEFINITION==================================================
const buttonClass = css({
    "&&&&& .icon": {
        opacity: 1.0
    }
})

//COMPONENT=================================================================
function OrderButton() {
    const initialState = {
        modalOpen: false,
        orderSuccess: false,
        orderFailed: false
    }

    function reducer(state, action) {
        switch (action.type) {
            case "START_ORDER":
                return {
                    ...state,
                    modalOpen: true
                }
            case "COMPLETE_ORDER":
                return {
                    ...state,
                    modalOpen: true,
                    orderSuccess: true
                }
            case "FAIL_ORDER":
                return {
                    ...state,
                    modalOpen: true,
                    orderFailed: true
                }
            case "CLOSE_ORDER":
                return {
                    ...state,
                    modalOpen: false
                }
            case "RESET_ORDER":
                return initialState;
            default:
                return state;
        }
    }

    const [state, dispatch] = useReducer(reducer, initialState);
    const { updatingCart, startOrder, loadCart } = useContext(CartContext);
    const { data, isLoggedIn } = useContext(CurrentUserContext);
    const [request, setRequest] = useState(null);
    const requestData = useRequestData(request);

    useEffect(() => {
        const { status } = requestData;
        if(status === 201){
            dispatch({type: "COMPLETE_ORDER"});
        }
        else if(status >= 400){
            dispatch({type: "FAIL_ORDER"});
        }
        else if(status >= 500){
            const { error } = requestData;
            throw {status, error};
        }
    }, [requestData])

    function executeOrder() {
        if(isLoggedIn){
            startOrder();
            dispatch({type: "START_ORDER"});
            setRequest({
                url: "/api/cart/order",
                method: "put",
                responseType: "json"
            })
        }
        else{
            window.location.replace("/login");
        }
    }

    function executeUnmount() {
        const { orderSuccess, orderFailed } = state;
        if(orderSuccess || orderFailed){
            loadCart();
            dispatch({type: "RESET_ORDER"});
        }
    }

    function renderButton() {
        return (
            <Button
                className={buttonClass}
                size="huge"
                fluid
                color="green"
                onClick={executeOrder}
                loading={updatingCart}
                disabled={updatingCart}
            >
                <Icon name="shopping basket" />
                Place Order
            </Button>
        )
    }

    function renderOrdering() {
        return (
            <Fragment>
                <Modal.Header>Placing your Order</Modal.Header>
                <Modal.Content>
                    <Message icon info>
                        <Icon name="sync alternate" loading />
                        <Message.Content>
                            <Message.Header>Just one second</Message.Header>
                            <Message.Content>We are placing your order.</Message.Content>
                        </Message.Content>
                    </Message>
                </Modal.Content>
            </Fragment>
        )
    }

    function renderSuccess() {
        return (
            <Fragment>
                <Modal.Header>Success</Modal.Header>
                <Modal.Content>
                    <Message icon success>
                        <Icon name="thumbs up" />
                        <Message.Content>
                            <Message.Header>Your order has been processed successfully.</Message.Header>
                            <Message.Content>{data.name}, thank you for buying with us. Since this is a demonstration project, please notice that your items will not be delivered.</Message.Content>
                        </Message.Content>
                    </Message>
                </Modal.Content>
            </Fragment>
        )
    }

    function renderFailure() {
        return (
            <Fragment>
                <Modal.Header>Error</Modal.Header>
                <Modal.Content>
                    <Message icon error>
                        <Icon name="exclamation triangle" />
                        <Message.Content>
                            <Message.Header>There was an error while placing your order.</Message.Header>
                            <Message.Content>{data.name}, please try again.</Message.Content>
                        </Message.Content>
                    </Message>
                </Modal.Content>
            </Fragment>
        )
    }

    function renderModalContent() {
        if(state.orderSuccess){
            return renderSuccess()
        }
        else if(state.orderFailed){
            return renderFailure()
        }
        else{
            return renderOrdering()
        }
    }

    function renderModalActions() {
        if(state.orderSuccess){
            return (
                <Modal.Actions>
                    <Button color="green" as={Link} to="/orders">Go to your orders</Button>
                    <Button color="blue" as={Link} to="">Continue shopping</Button>
                </Modal.Actions>
            )
        }
        else if(state.orderFailed){
            return (
                <Modal.Actions>
                    <Button color="blue" onClick={() => dispatch({type: "CLOSE_ORDER"})}>Close this window</Button>
                </Modal.Actions>
            )
        }
        else{
            return null;
        }
    }

    function render() {
        return (
            <Modal
                trigger={renderButton()}
                open={state.modalOpen}
                onUnmount={executeUnmount}
                closeOnEscape={false}
                closeOnDimmerClick={false}
            >
                {renderModalContent()}
                {renderModalActions()}
            </Modal>
        )
    }

    return render()
}

//EXPORT COMPONENT==========================================================
export default OrderButton;