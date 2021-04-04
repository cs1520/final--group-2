/**
 * Limits the frequency at which an event function
 * can be invoked.
 *
 * e.g. 20 events over 2 seconds might only result in one invocation
 * (once a certain time passes with no more events)
 *
 * @param callback - The callback function to invoke
 * @param delay - The amount of delay to wait before invoking
 * @returns an intermediary function that can be used to emit an event
 */
export function debounce(callback, delay) {
	let timeout = null;

	// any args passed to this function are sent to the callback
	return function(...args) {
		// clear the existing timeout (if present)
		clearTimeout(timeout);
		// create a new timeout to invoke the callback
		timeout = setTimeout(() => {
			callback(...args);
		}, delay);
	};
}
