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

/**
 * Obtains an object/dict of all storage values with the given
 * prefix value.
 *
 * e.g. if the prefix is "data-" and localStorage contains
 *   { "data-hello": "world", "data-apple": "monch", "unrelated-value": "hi" }
 * then the returned value will be
 *   { "hello": "world", "apple": "monch" }
 *
 * @param prefix - The prefix to search for
 * @returns A dict of all keys matching the prefix
 */
export function allStorage(prefix) {
	let values = {};

	// get all keys from localStorage
	let keys = Object.keys(localStorage);
	for (let key of keys) {
		// if key doesn't have prefix, ignore
		if (!key.startsWith(prefix))
			continue;

		// remove prefix from key & insert in values
		let valueKey = key.substr(prefix.length);
		values[valueKey] = localStorage.getItem(key);
	}

	return values;
}
