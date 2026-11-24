# Example: a silently dropped routing signal

A job submitted through the normal queue with `route=priority` reaches the standard worker. Keep the job, revision, and queue conditions fixed, changing only the route in the control.

| Hypothesis | Prediction for the priority input before any patch |
| --- | --- |
| The queue adapter drops the route | Request has `priority`, dequeued record has no route, consumer chooses `standard`. |
| The consumer ignores a valid route | Request and dequeued record both have `priority`, consumer still chooses `standard`. |

Check the received value and chosen worker on the same job. Submit the paired control `route=standard` through the same entry point. Suppose the priority request loses its route in the queue round trip while the standard request still reaches the standard worker. This supports an adapter defect and falsifies the prediction that the consumer received the priority value on that run.

If repair is authorized, preserve the route at the earliest dropping adapter. Rerun both inputs through the normal queue. The priority job must retain `priority` on dequeue and dispatch to the priority worker. The standard control must still dispatch to the standard worker. A passing serialization test alone would leave the consumer effect unobserved. If the value now arrives but dispatch is still standard, record the first repair and investigate the remaining seam instead of claiming the original symptom is fixed.
