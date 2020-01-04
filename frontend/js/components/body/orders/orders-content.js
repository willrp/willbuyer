//IMPORT EXTERNAL COMPONENTS================================================
import React, { Fragment, useState, useEffect } from "react";
import { Segment, Label, Pagination } from "semantic-ui-react";

//IMPORT INTERNAL COMPONENTS================================================
import ContentLoading from "components/util/content-loading";
import NoContent from "components/util/no-content";
import Counter from "./counter";
import DateRange from "./date-range";
import PageSizeSelect from "./page-size-select";
import OrdersGrid from "./orders-grid";

//IMPORT HOOKS==============================================================
import useRequestData from "hooks/request-data";
import useDidMount from "hooks/did-mount";

//IMPORT EXTERNAL FUNCTIONS=================================================
import { css } from "emotion";

//STYLE CLASSES DEFINITION==================================================
const segmentsClass = css({
    "&&&&&": {
        marginBottom: "0px"
    },
    "&&&&& .segment": {
        display: "flex",
        alignItems: "center",
        justifyContent: "center"
    },
    "&&&&& .dateRangeClass": {
        padding: "0"
    }
})

const paginationClass = css({
    "&&&&&": {
        display: "flex",
        justifyContent: "center"
    }
})

const pageItem = css({
    "&&&&&.active": {
        backgroundColor: "deepskyblue"
    }
})

//COMPONENT=================================================================
function OrdersContent({ pages, total, orders, pageSize }) {
    const [page, setPage] = useState(1);
    const [currentPageSize, setCurrentPageSize] = useState(pageSize);
    const [dateRange, setDateRange] = useState({start: null, end: null});

    const [currentLoading, setCurrentLoading] = useState(false);
    const [totalPages, setTotalPages] = useState(pages);
    const [currentTotal, setCurrentTotal] = useState(total);
    const [currentOrders, setCurrentOrders] = useState(orders);

    const didMount = useDidMount();
    const [request, setRequest] = useState(null);
    const requestData = useRequestData(request);

    useEffect(() => {
        if(!didMount){
            setCurrentLoading(true);
            const { start, end } = dateRange;
            const datespan = (start !== null && end !== null) ? dateRange : null
            setRequest({
                url: "/api/order/user",
                method: "post",
                responseType: "json",
                data: {
                    page: page,
                    page_size: pageSize,
                    datespan: datespan
                }
            })
        }
    }, [page, pageSize, dateRange.start, dateRange.end])

    useEffect(() => {
        const { loading, data, status, error } = requestData;
        if(!loading){
            if(status === 200 && data !== null) {
                setCurrentTotal(data.total);
                setTotalPages(data.pages);
                setCurrentOrders(data.orders);
            }
            else if(status === 204 && data === null) {
                setCurrentTotal(0);
                setCurrentOrders(null);
            }
            else if(status >= 400 && error !== null){
                throw {status, error};
            }
            setCurrentLoading(false);
        }
    }, [requestData])

    function changePage(e, { activePage }) {
        setPage(activePage);
    }

    function changePageSize(e, { value }) {
        setPage(1);
        setCurrentPageSize(value);
    }    

    function changeDate({ startDate, endDate }) {
        setPage(1);
        setDateRange({
            start: startDate.format("YYYY-MM-DD"),
            end: endDate.format("YYYY-MM-DD")
        });
    }

    function renderOrders() {
        const { status } = requestData;
        if(currentLoading) {
            return <ContentLoading />
        }
        else if(status === 204 && currentOrders === null) {
            return <NoContent message="No orders found. Please change the date range." />
        }
        else{
            return (
                <Fragment>
                    <OrdersGrid orders={currentOrders} />
                    <div className={paginationClass} >
                        <Pagination activePage={page.toString()} totalPages={totalPages} onPageChange={changePage} pageItem={{className: pageItem}} />
                    </div>
                </Fragment>
            )
        }
    }

    function render() {
        return (
            <Fragment>
                <Segment.Group horizontal className={segmentsClass}>
                    <Segment>
                        <Counter total={currentTotal} />
                    </Segment>
                    <Segment>
                        <Label attached="top left">Date Range: </Label>
                        <Segment className="dateRangeClass">
                            <DateRange onDatesChange={changeDate} />
                        </Segment>
                    </Segment>
                    <Segment>
                        <Label attached="top left">Orders per page: </Label>
                        <PageSizeSelect value={currentPageSize} pageList={[6, 12, 18, 24, 30]} onChange={changePageSize} />
                    </Segment>
                </Segment.Group>
                {renderOrders()}
            </Fragment>
        )
    }

    return render()
}

//EXPORT COMPONENT==========================================================
export default OrdersContent;