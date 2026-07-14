"""
Stub module for LLM-based OCR post-correction.
This acts as a placeholder for the final LLM integration.
"""

def correct_ocr_text(text: str, confidence: float, block_id: str, threshold: float = 0.95) -> str:
    """
    Applies constrained post-correction to the OCR text using an LLM.
    
    To save costs and time, this only triggers if the OCR confidence is below the threshold.
    The LLM must only correct character-level errors and must not summarize or paraphrase.
    
    Args:
        text: The raw OCR text block.
        confidence: The average confidence score from Tesseract (0.0 to 1.0).
        block_id: The ID of the block (for logging purposes).
        threshold: The confidence threshold below which the LLM is triggered.
        
    Returns:
        The corrected text (or the original text if confidence >= threshold).
    """
    if confidence < threshold:
        # TODO: Boss to inject actual LLM API call here!
        # Example prompt to use: 
        # "You are a legal OCR corrector. Fix only obvious character recognition errors. 
        # Do not change the phrasing, do not summarize, do not translate. 
        # Output ONLY the corrected text: {text}"
        
        print(f"    [LLM TRIGGERED] Confidence {confidence:.3f} < {threshold} for block {block_id}.")
        print(f"    -> [STUB] Skipping actual LLM call. Returning original text.")
        
        return text
    
    return text
