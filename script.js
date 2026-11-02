/* Presentation script, slide by slide. Used by the deck's Notes and by notes/index.html.
 * Numbers come from amazon_synthetic_1500_orders.xlsx (see scripts/analysis.json). */
window.SCRIPT=[
{id:'globe',title:'Cash or click?',time:'0:20',text:[
'Good morning everyone. Every time someone shops online, they make one small choice at checkout: pay now, or pay cash when the parcel arrives.',
'Our project asks a simple question: does that choice change how many orders actually go through, and how much revenue a company keeps? Let’s find out.']},
{id:'cart',title:'Some orders have commitment issues',time:'0:30',text:[
'Here’s the problem. Out of 1,500 orders, 171 were cancelled. That’s 11.4%.',
'But split it by payment mode and the picture changes. Cash on delivery orders cancel 20.3% of the time. Prepaid orders cancel only 7.4%. So roughly one in five COD orders never turns into revenue, compared with about one in fourteen prepaid orders.']},
{id:'data',title:'1,500 orders. 12 cities.',time:'0:25',text:[
'Our data is 1,500 orders from January to September 2025, spread across 12 Indian cities, about 125 orders each, so no single city dominates.',
'One important point: this is a synthetic course dataset. It lets us demonstrate the statistical method, but it is not real Amazon performance.']},
{id:'lanes',title:'Six ways to pay. Two lanes to compare.',time:'0:25',text:[
'Customers used six payment methods. Cash on delivery has 469 orders.',
'The other five, UPI, credit card, debit card, net banking and wallet, are all paid upfront, so we group them as prepaid: 1,031 orders. UPI alone is the biggest single method at 547.',
'From here on, we compare two lanes: COD versus prepaid.']},
{id:'tend',title:'The mean has expensive friends',time:'0:30',text:[
'Next, how big is a typical order? The mean is ₹1,688, but the median is only ₹1,067. That’s a gap of about ₹620.',
'That happens because a few very large baskets pull the average up. So when we describe a typical customer, the median is the better number. The mean is still useful when we talk about total revenue.']},
{id:'disp',title:'How spread out are order values?',time:'0:30',text:[
'How spread out are order values? We use variance and standard deviation.',
'For COD, the standard deviation is ₹1,722. For prepaid, it’s ₹1,631. Variance is the same idea but measured in rupees squared, so the standard deviation is easier to read.',
'In simple terms, a typical order sits about ₹1,600 to ₹1,700 away from its group’s average.']},
{id:'corr',title:'Payment and completion. A negative link.',time:'0:40',text:[
'Now, is payment mode linked to whether an order is completed? We code X as 1 for COD and 0 for any prepaid method, and Y as 1 if the order was completed and 0 if it was cancelled.',
'Using the counts, 469 COD orders, 1,329 completed orders, and 374 that are both, the covariance comes out to minus 0.0277 and the correlation is minus 0.19.',
'The sign is what matters: it’s negative. Choosing COD goes with fewer completed orders.']},
{id:'bayes',title:'31% of orders. 56% of cancellations.',time:'0:35',text:[
'Let’s focus only on COD. 20.3% of COD orders get cancelled.',
'Now flip the question using Bayes’ theorem: if an order is cancelled, how likely is it to be COD? The answer is 55.6%.',
'So COD is only 31% of all orders, but it accounts for more than half of all cancellations.']},
{id:'bin',title:'15 orders. How many cancel?',time:'0:40',text:[
'Let’s make that practical with the binomial distribution. Take a batch of 15 orders. “Success” here simply means an order gets cancelled.',
'For COD the probability is 0.2026; for prepaid, 0.0737. In 15 COD orders we expect about 3 cancellations. In 15 prepaid orders, only about 1.',
'The chance of exactly 3 cancellations is 25% for COD, but just 7.3% for prepaid.']},
{id:'welch',title:'Do COD orders have higher value?',time:'0:35',text:[
'One possible defence of COD: maybe COD buyers place bigger orders, so they’re worth the risk. We test that.',
'COD orders average ₹1,725 and prepaid orders ₹1,672. Our z calculated is 0.57, and the z critical value at 5% significance is 1.645.',
'Since 0.57 is less than 1.645, we do not reject the null hypothesis. COD orders are not significantly bigger.']},
{id:'ztest',title:'Does COD really cancel more?',time:'0:35',text:[
'Now the main test: does COD really cancel more? COD cancels 20.3%, prepaid 7.4%.',
'Using the two-proportion z-test, z calculated is 7.28, far above the critical value of 1.645. So we reject the null hypothesis.',
'COD orders cancel significantly more than prepaid orders, and the difference is not down to chance.']},
{id:'find',title:'Make prepaid the easy choice.',time:'0:45',text:[
'So what should a company actually do with this? Our data suggests prepaid customers are more valuable, so the goal is to move more customers toward prepaying.',
'We wouldn’t ban cash on delivery, because that risks losing buyers. Instead, make prepaid the easier and cheaper choice: a small discount for paying online, prepaid selected by default at checkout, and a small fee on COD.',
'Then test it. If prepaid share goes up without hurting conversion, revenue goes up. And since this data is synthetic, the next step is to confirm it with real orders.']},
{id:'end',title:'Thank you.',time:'0:10',text:[
'That’s our analysis. Cash or click? The click wins.',
'Thank you. We’re happy to take your questions.']}
];
