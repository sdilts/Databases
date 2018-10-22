(ns word-count.core)
(require '[opennlp.nlp :as nlp])
(use 'local-file)

(def tokenize-fn (nlp/make-tokenizer (str (project-dir) "/resources/en-token.bin")))

(defn count-items [word-list]
  (reduce (fn [mp item]
            (let [count (get mp item 0)]
              (assoc mp item (inc count))))
          {}
          word-list))

(defn tokenize-string [string]
  (tokenize-fn string))

(defn total-words [mp]
  (loop [sum 0
         ]
    (recur (+ (second value sum) mp))))
