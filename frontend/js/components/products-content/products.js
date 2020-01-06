//IMPORT EXTERNAL COMPONENTS================================================
import React, { Fragment, useState, useContext, useEffect } from "react";
import { useLocation } from "react-router";
import { Segment, Label, Pagination, Responsive } from "semantic-ui-react";

//IMPORT INTERNAL COMPONENTS================================================
import ContentLoading from "components/util/content-loading";
import NoContent from "components/util/no-content";
import Counter from "./counter";
import PriceRange from "./price-range";
import PageSizeSelect from "./page-size-select";
import ProductGrid from "./product-grid";

//IMPORT CONTEXTS===========================================================
import { SidebarContext } from "contexts/sidebar-context";

//IMPORT HOOKS==============================================================
import useRequestData from "hooks/request-data";
import useDidMount from "hooks/did-mount";
import useIsPhone from "hooks/is-phone";

//IMPORT EXTERNAL FUNCTIONS=================================================
import { css } from "emotion";
import { pick } from "lodash";
import queryString from "query-string";

//IMPORT INTERNAL FUNCTIONS=================================================
import validatePriceRange from "lib/validate-price-range";

// STYLE CLASSES DEFINITION=================================================
const segmentsClass = css({
    "&&&&&": {
        marginBottom: "0px"
    },
    "&&&&& .segment": {
        display: "flex",
        alignItems: "center",
        justifyContent: "center"
    }
})

const rangeClass = css({
    "&&&&&": {
        flexGrow: 100,
        paddingLeft: "2em",
        paddingRight: "2em"
    }
})

const stackedClass = css({
    "&&&&&": {
        margin: 0,
        paddingLeft: "2em",
        paddingRight: "2em"
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
function Products({ url, pricerange, total }) {
    const { search } = useLocation();
    const query = queryString.parse(search);
    const queryRange = validatePriceRange(pick(query, ["min", "max"]));
    const pickedrange = (queryRange === null) ? pricerange : queryRange;

    const didMount = useDidMount();
    const [currentUrl] = useState(url);
    const [page, setPage] = useState(1);
    const [pageSize, setPageSize] = useState(20);
    const [totalProducts, setTotalProducts] = useState(total);

    const [outerRequest, setOuterRequest] = useState(null);
    const outerRequestData = useRequestData(outerRequest);
    const { sidesessions, updateItems } = useContext(SidebarContext);

    const isPhone = useIsPhone();

    useEffect(() => {
        if(!didMount && currentUrl === url) {
            setOuterRequest({
                url: url,
                method: "post",
                responseType: "json",
                data: {
                    pricerange: pickedrange
                }
            })
        }
    }, [pickedrange.min, pickedrange.max])

    useEffect(() => {
        const { data, status, error } = outerRequestData;
        if(status === 200 && data !== null) {
            const { sessions, brands, kinds, total } = data;
            const sessiondata = (sessions === undefined) ? sidesessions : sessions;
            setTotalProducts(total);
            updateItems(sessiondata, brands, kinds);
        }
        else if(status === 204 && data === null) {
            setTotalProducts(0);
        }
        else if((status === 400 || status >= 500) && data === null) {
            throw {status, error};
        }
    }, [outerRequestData])

    const [request, setRequest] = useState(null);
    const requestData = useRequestData(request);

    useEffect(() => {
        if(currentUrl === url) {
            setRequest({
                url: `${url}/${page}`,
                method: "post",
                responseType: "json",
                data: {
                    pagesize: pageSize,
                    pricerange: pickedrange
                }
            })
        }        
    }, [page, pageSize, pickedrange.min, pickedrange.max])

    function changePageSize(e, { value }) {
        setPage(1);
        setPageSize(value);
    }

    function changePage(e, { activePage }) {
        setPage(activePage);
    }

    function renderProducts() {
        const { data, status, loading } = requestData;
        if(loading === true) {
            return <ContentLoading />
        }
        else if(status === 204 || data === null) {
            return <NoContent message="No products found. Please change the price range." />
        }
        else{
            const { products } = data;
            const totalPages = Math.ceil(totalProducts / pageSize)
            return (
                <Fragment>
                    <ProductGrid products={products} />
                    <div className={paginationClass}>
                        <Pagination
                            activePage={page.toString()}
                            totalPages={totalPages}
                            onPageChange={changePage}
                            pageItem={{className: pageItem}}
                            boundaryRange={(isPhone) ? 0 : 1}
                            ellipsisItem={(isPhone) ? null : undefined}
                        />
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
                        <Counter total={totalProducts} />
                    </Segment>
                    <Responsive
                        as={Segment}
                        minWidth={Responsive.onlyTablet.minWidth}
                        className={rangeClass}
                    >
                        <Label attached="top left">Price range: </Label>
                        <PriceRange pricerange={pricerange} pickedrange={pickedrange} executeOnChange={() => setPage(1)} />
                    </Responsive>
                    <Segment>
                        <Label attached="top left">Products per page: </Label>
                        <PageSizeSelect value={pageSize} pageList={[10, 20, 30, 40, 50]} onChange={changePageSize} />
                    </Segment>
                </Segment.Group>
                <Responsive
                    {...Responsive.onlyMobile}
                    as={Segment}
                    className={stackedClass}
                >
                    <Label attached="top left">Price range: </Label>
                    <PriceRange pricerange={pricerange} pickedrange={pickedrange} executeOnChange={() => setPage(1)} />
                </Responsive>
                {renderProducts()}
            </Fragment>
        )
    }

    return render()
}

//EXPORT COMPONENT==========================================================
export default Products;