from video.framer import convert_video_to_frames, convert_video_to_frames_and_crop
from model.slides_model import create_model, save_model, load_model, compare_screens
from model.slides_model_test import get_text_data, get_predictions, get_scores
from model.interventions_model import get_interventions
import csv


def gen_frames(train_video, frame_type="frame"):
    """
        frame_type = ("frame" || "test")
    """
    convert_video_to_frames("data/"+train_video, "slides", frame_type, frame_rate_value=5) # Full frame
    convert_video_to_frames_and_crop("data/"+train_video, "intervention", frame_type, frame_rate_value=5) # Cropped frame


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
    return model, base_model

def predict_slides(model, base_model, i):
    # Test model
    test_x, test_y = get_text_data(base_model, "data/slides_data/test/testing"+str(i)+".csv")
    # # Predictions
    predictions = get_predictions(model, test_x)
    return predictions


if __name__ == '__main__':
    print("=================> Generating video frames")
    # gen_frames("slides_data/training/Training.mp4", "frame")
    # gen_frames("slides_data/test/Test.mkv", "test")
    # gen_frames("interventions_data/training/trim5", "frame")
    print("=================> Generating Slides Model")
    """
    model, base_model = slides_model("slides", False)
    slides = []
    for i in range(1,9):
        r = predict_slides(model, base_model, i)
        print(r)
        slides = list(slides) + list(r)
    with open("data/out/slides.csv", "w", newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Image_ID", "Class"])
        for i in range(0, len(slides)):  
            number = 1475 + i
            writer.writerow([number, slides[i]])
    """
    # Posible output de log conjunto: "time, is_presenting, slide_changed_recently, interventor"
    # print("=================> Get interventions logs")
    # get_interventions('data/frames/intervention_frames/training', 'intervention_logs.csv')
    print("Done.")

    changes = compare_screens('data/out/slides.csv')
    with open("data/out/changes.csv", "w", newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Image_ID", "Similarity"])
        for i in range(0, len(changes)):  
            writer.writerow([changes[i][0], changes[i][1]])
