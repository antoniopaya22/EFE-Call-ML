from video.framer import convert_video_to_frames, convert_video_to_frames_and_crop
from model.slides_model import create_model, save_model, load_model
from model.slides_model_test import get_text_data, get_predictions, get_scores
from model.interventions_model import get_interventions


def gen_frames(train_video, frame_type="frame"):
    """
        frame_type = ("frame" || "test")
    """
    convert_video_to_frames("data/"+train_video, "slides", frame_type, frame_rate_value=5) # Full frame
    #convert_video_to_frames_and_crop("data/"+train_video, "intervention", frame_type, frame_rate_value=5) # Cropped frame


def slides_model(model_name, train_model=False):
    data_location = model_name+"_data"
    # Train model
    if train_model:
        model, base_model = create_model("data/"+data_location+"/training/mapping.csv")
        save_model(model, "data/models/"+model_name+"_model.h5")
        del model
        save_model(base_model, "data/models/"+model_name+"_model_base.h5")
        del base_model
    # Load model from file
    model = load_model("data/models/"+model_name+"_model.h5")
    base_model = load_model("data/models/"+model_name+"_model_base.h5")
    # Test model
    test_x, test_y = get_text_data(base_model, "data/"+data_location+"/test/testing.csv")
    # # Scores
    # scores = get_scores(model, test_x, test_y)
    # print("======================================================")
    # print("%s: %.2f%%" % (model.metrics_names[1], scores[1] * 100))
    # print("======================================================")
    # # Predictions
    predictions = get_predictions(model, test_x)
    return predictions
    # print("======================================================")
    # print(predictions)
    # print("======================================================")


if __name__ == '__main__':
    print("=================> Generating video frames")
    # gen_frames("slides_data/training/TrainVideo.mkv", "frame")
    gen_frames("slides_data/test/Test.mkv", "test")
    # gen_frames("interventions_data/training/trim5", "frame")
    # print("=================> Generating Slides Model")
    # slides = slides_model("slides", False)
    # print(slides)
    # Posible output de log conjunto: "time, is_presenting, slide_changed_recently, interventor"
    # print("=================> Get interventions logs")
    # get_interventions('data/frames/intervention_frames/training', 'intervention_logs.csv')
    print("Done.")
